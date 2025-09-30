import unittest

from src.lab1.calculator import calc


class CalculatorTestCase(unittest.TestCase):
    def test_1(self):
        self.assertEqual(calc("1", "2", "+"), 3)

    def test_2(self):
        self.assertEqual(calc("1", "2", "-"), -1)

    def test_3(self):
        self.assertEqual(calc("10", "2", "*"), 20)

    def test_4(self):
        self.assertEqual(calc("10", "2", "/"), 5)

    def test_5(self):
        self.assertEqual(calc("1.2", "5", "*"), 6)

    def test_6(self):
        self.assertEqual(calc("2", "2", "/"), 1)

    def test_7(self):
        self.assertEqual(calc("5", "150", "*"), 750)

    def test_8(self):
        self.assertEqual(calc("112324", "21212324", "+"), 21_324_648)

    def test_9(self):
        self.assertEqual(calc("1", "1", "*"), 1)

    def test_10(self):
        self.assertEqual(calc("1", "0", "/"), "Error")
