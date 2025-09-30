import unittest

from src.lab4.first import Films, Users


class FirstTestCase(unittest.TestCase):
    def test_class_films(self):
        films = Films()
        movies = [
            (0, "Тетрадь смерти"),
            (1, "Атака титанов"),
            (2, "Наруто"),
            (3, "Истребитель демонов"),
            (4, "Необъятный океан"),
            (5, "Sword Art Online"),
        ]
        for movie in movies:
            films.add_film(*movie)
        self.assertEqual(films.get_film_by_id(0), "Тетрадь смерти")
        self.assertEqual(films.get_film_by_id(3), "Истребитель демонов")
        self.assertEqual(films.get_film_by_id(5), "Sword Art Online")

    def test_class_users(self):
        users = Users()
        usersList = [{1, 2, 3, 4, 6}, {1, 2, 3, 7}, {4, 5, 6}, {1}, {2}, {2, 3, 4, 5}]
        for user in usersList:
            users.add_user(user)
        self.assertEqual(users.get_reco({5, 6}), 4)
        self.assertEqual(users.get_reco({2, 3, 5}), 4)
        self.assertEqual(users.get_reco({1, 2, 3, 6}), 4)
