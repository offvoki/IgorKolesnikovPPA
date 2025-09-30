"""Movie recommendation system"""

from typing import Dict, List, Set, Tuple


class Films:
    """Class for managing films"""

    def __init__(self) -> None:
        """Initialize"""
        self.films: Dict[int, str] = {}

    def add_film(self, id: int, name: str) -> None:
        """Add a film to the list"""
        self.films[id] = name

    def get_film_by_id(self, id: int) -> str:
        """Get a film name by id. Always returns str (empty if not found)."""
        return self.films.get(id, "")


class Users:
    """Class with all users information"""

    def __init__(self) -> None:
        """Initialize"""
        self.users: List[Set[int]] = []

    def add_user(self, watched: Set[int]) -> None:
        """Add a user"""
        self.users.append(watched)

    def get_reco(self, watched: Set[int]) -> int:
        """Get film recommendation id"""
        if not watched:
            # если пользователь ничего не смотрел — рекомендуем самый частый у других
            counts: Dict[int, int] = {}
            for s in self.users:
                for film in s:
                    counts[film] = counts.get(film, 0) + 1
            # если пользователей нет — вернём "нет рекомендации"
            return max(counts, key=lambda k: counts[k]) if counts else -1

        films_for_reco: List[Tuple[float, int]] = []
        for s in self.users:
            k = len(watched & s) / len(watched)
            for j in s - watched:
                films_for_reco.append((k, j))
        films_for_reco.sort(key=lambda x: -x[0])
        return films_for_reco[0][1] if films_for_reco else -1


if __name__ == "__main__":
    films = Films()
    users = Users()

    with open("films.txt", "r") as f:
        for line in f.read().splitlines():
            if not line:
                continue
            fid_str, name = line.split(",", 1)
            films.add_film(int(fid_str), name)

    with open("users.txt", "r") as f:
        for line in f.read().splitlines():
            if not line:
                continue
            users.add_user(set(map(int, line.split(","))))

    watched = set(map(int, input().split(",")))
    film_id = users.get_reco(watched)
    print(films.get_film_by_id(film_id))
