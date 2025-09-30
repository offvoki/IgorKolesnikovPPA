# db.py
from typing import Any, Dict, List, Optional
from uuid import uuid4

from sqlalchemy import Integer, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase):
    pass


class Movie(Base):
    __tablename__ = "movies"
    # id хранится как hex-строка UUID (32 символа)
    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    director: Mapped[str] = mapped_column(String(100), nullable=False)
    length: Mapped[str] = mapped_column(String(8), nullable=False)  # "HH:MM:SS"
    rating: Mapped[int] = mapped_column(Integer, nullable=False)


# Вспомогательные функции


def hex_to_int(h: str) -> int:
    return int(h, 16)


def int_to_hex(i: int) -> str:
    return hex(i)[2:]


def uuid_hex() -> str:
    return uuid4().hex  # 32-символьная hex-строка


def row_to_dict(m: Movie) -> Dict[str, Any]:
    return {
        "id": hex_to_int(m.id),
        "title": m.title,
        "year": m.year,
        "director": m.director,
        "length": m.length,
        "rating": m.rating,
    }


# Класс EngineWorker


class EngineWorker:
    def __init__(self, path: str):
        self.engine = create_engine(path, future=True)
        Base.metadata.create_all(self.engine)

    # GET /api/movies
    def movies_list(self) -> Dict[str, List[Dict[str, Any]]]:
        with Session(self.engine) as session:
            rows = session.query(Movie).all()
        return {"list": [row_to_dict(m) for m in rows]}

    # POST /api/movies
    def add_movie(self, movie: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        new_id_hex = uuid_hex()
        with Session(self.engine) as session:
            m = Movie(
                id=new_id_hex,
                title=movie["title"],
                year=movie["year"],
                director=movie["director"],
                length=movie["length"],
                rating=movie["rating"],
            )
            session.add(m)
            session.commit()
        saved = {**movie, "id": hex_to_int(new_id_hex)}
        return {"movie": saved}

    # GET /api/movies/:id
    def find_movie(self, movie_id: int) -> Optional[Dict[str, Dict[str, Any]]]:
        id_hex = int_to_hex(movie_id)
        with Session(self.engine) as session:
            m = session.get(Movie, id_hex)
        return {"movie": row_to_dict(m)} if m else None

    # PATCH /api/movies/:id
    def patch_movie(self, movie_id: int, movie_patch: Dict[str, Any]) -> Optional[Dict[str, Dict[str, Any]]]:
        id_hex = int_to_hex(movie_id)
        with Session(self.engine) as session:
            m = session.get(Movie, id_hex)
            if not m:
                return None
            # обновляем только переданные поля
            for k in ("title", "year", "director", "length", "rating"):
                if k in movie_patch:
                    setattr(m, k, movie_patch[k])
            session.commit()
            return {"movie": row_to_dict(m)}

    # DELETE /api/movies/:id
    def delete_movie(self, movie_id: int) -> bool:
        id_hex = int_to_hex(movie_id)
        with Session(self.engine) as session:
            m = session.get(Movie, id_hex)
            if not m:
                return False
            session.delete(m)
            session.commit()
            return True
