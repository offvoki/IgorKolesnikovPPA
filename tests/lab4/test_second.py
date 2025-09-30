import unittest

from src.lab4.second import Society


class SecondTestCase(unittest.TestCase):
    def test_add_person(self):
        society = Society(["50"])
        society.add_person("Колесников Игорь Евгеньевич, 20")
        self.assertEqual(society.groups, {0: [[20, "Колесников", "Игорь", "Евгеньевич"]], 1: []})
        society.add_person("Илон Рив Маск, 52")
        self.assertEqual(society.groups, {0: [[20, "Колесников", "Игорь", "Евгеньевич"]], 1: [[52, "Илон", "Рив", "Маск"]]})

    def test_print(self):
        society = Society(["50"])
        society.add_person("Колесников Игорь Евгеньевич, 20")
        society.add_person("Илон Рив Маск, 52")
        self.assertEqual(society.print(), """51+: Илон Рив Маск (52)\n0-50: Колесников Игорь Евгеньевич (20)\n""")
