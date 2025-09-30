import re
from typing import Final

from flask import Flask, jsonify, request

from .config import DATABASE_PATH as dbpath
from .db import EngineWorker

app: Flask = Flask(__name__)
engworker: EngineWorker = EngineWorker(dbpath)

LENGTH_RE: Final[re.Pattern[str]] = re.compile(r"^\d{2}:\d{2}:\d{2}$")

__all__ = ["app"]


def error(status: int, reason: str):
    return jsonify({"status": status, "reason": reason}), status


def validate_fields(payload: dict, partial: bool = False):
    # partial=True -> валидируем только переданные поля
    # обязательные поля в POST
    required = ["title", "year", "director", "length", "rating"]
    if not partial:
        for f in required:
            if f not in payload:
                return error(400, f"Field '{f}' is required")

    if "title" in payload:
        title = payload["title"]
        if not isinstance(title, str) or not (1 <= len(title) <= 100):
            return error(400, "Field 'title' must be a non-empty string up to 100 chars")

    if "year" in payload:
        year = payload["year"]
        if not isinstance(year, int) or not (1900 <= year <= 2100):
            return error(400, "Field 'year' should be between 1900 and 2100")

    if "director" in payload:
        director = payload["director"]
        if not isinstance(director, str) or not (1 <= len(director) <= 100):
            return error(400, "Field 'director' must be a non-empty string up to 100 chars")

    if "length" in payload:
        length = payload["length"]
        if not isinstance(length, str) or not LENGTH_RE.match(length):
            return error(400, "Field 'length' must be in 'HH:MM:SS' format")
        # Дополнительная проверка диапазонов
        try:
            hh, mm, ss = map(int, length.split(":"))
            if not (0 <= hh <= 99 and 0 <= mm < 60 and 0 <= ss < 60):
                return error(400, "Field 'length' has invalid time components")
        except Exception:
            return error(400, "Field 'length' must be in 'HH:MM:SS' format")

    if "rating" in payload:
        rating = payload["rating"]
        if not isinstance(rating, int) or not (0 <= rating <= 10):
            return error(400, "Field 'rating' should be between 0 and 10")

    return None


@app.route("/api/movies", methods=["GET"])
def get_all_movies():
    data = engworker.movies_list()
    return jsonify(data), 200


@app.route("/api/movies", methods=["POST"])
def add_movie():
    body = request.get_json(silent=True) or {}
    movie = body.get("movie")
    if not isinstance(movie, dict):
        return error(400, "Root key 'movie' with object value is required")

    err = validate_fields(movie, partial=False)
    if err:
        return err

    try:
        saved = engworker.add_movie(movie)
        return jsonify(saved), 200
    except Exception as e:
        return error(500, f"{e}")


@app.route("/api/movies/<int:movie_id>", methods=["GET"])
def find_movie_by_id(movie_id: int):
    found = engworker.find_movie(movie_id)
    if not found:
        return "", 404
    return jsonify(found), 200


@app.route("/api/movies/<int:movie_id>", methods=["PATCH"])
def patch_movie_by_id(movie_id: int):
    body = request.get_json(silent=True) or {}
    movie_patch = body.get("movie")
    if not isinstance(movie_patch, dict):
        return error(400, "Root key 'movie' with object value is required")

    err = validate_fields(movie_patch, partial=True)
    if err:
        return err

    updated = engworker.patch_movie(movie_id, movie_patch)
    if not updated:
        return "", 404
    return jsonify(updated), 200


@app.route("/api/movies/<int:movie_id>", methods=["DELETE"])
def delete_movie_by_id(movie_id: int):
    try:
        ok = engworker.delete_movie(movie_id)
        if not ok:
            return "", 404
        # ТЗ: 202 Accepted
        return "", 202
    except Exception as e:
        return error(500, f"{e}")


if __name__ == "__main__":
    app.run(debug=True)
