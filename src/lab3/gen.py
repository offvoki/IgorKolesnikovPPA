"""Модуль для генерации примеров судоку"""

from random import randint


class Sudoku:
    """Класс для генерации судоку"""

    def __init__(self, n: int):
        """Инит класса

        Args:
            n (int): количество заполненных элементов
        """
        self.delete = max(0, 81 - n)
        with open("src/lab3/sample.grid", "r") as f:
            self.grid = list(map(lambda x: list(x.strip()), f.readlines()))

    def display(self) -> None:
        """Вывод Судок"""
        width = 2
        line = "+".join(["-" * (width * 3)] * 3)
        for row in range(9):
            print("".join(self.grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)))
            if str(row) in "25":
                print(line)
        print()

    def T(self) -> None:
        """Транспонирования"""
        self.grid = list(map(lambda x: list(x), zip(*self.grid)))

    def small_swap_rows(self) -> None:
        """Поменять местами 2 строчки в одной блочной строке"""
        area = randint(0, 2)
        line1 = randint(0, 2)
        line2 = randint(0, 2)
        while line1 == line2:
            line2 = randint(0, 2)
        self.grid[area * 3 + line1], self.grid[area * 3 + line2] = (
            self.grid[area * 3 + line2],
            self.grid[area * 3 + line1],
        )

    def small_colums_swap(self) -> None:
        """Поменять местами 2 столбика в одном блочном столбце"""
        self.T()
        self.small_swap_rows()
        self.T()

    def rows_swap(self) -> None:
        """Поменять местами блочные строки"""
        area1 = randint(0, 2)
        area2 = randint(0, 2)
        while area1 == area2:
            area2 = randint(0, 2)
        for i in range(3):
            self.grid[area1 * 3 + i], self.grid[area2 * 3 + i] = self.grid[area2 * 3 + i], self.grid[area1 * 3 + i]

    def columns_swap(self) -> None:
        """Поменять местами блочные столбцы"""
        self.T()
        self.rows_swap()
        self.T()

    def mix(self, cnt=10) -> None:
        """Функция для перемешивания сетки

        Args:
            cnt (int, optional): Количество применяемых функций
        """
        funs = [self.T, self.small_swap_rows, self.small_colums_swap, self.rows_swap, self.columns_swap]
        for i in range(cnt):
            fun = randint(0, len(funs) - 1)
            funs[fun]()

    def delete_cells(self) -> None:
        """Фукнция для удаления полей"""
        bool_grid = [[0 for i in range(9)] for j in range(9)]
        while self.delete:
            x, y = randint(0, 8), randint(0, 8)
            while bool_grid[x][y]:
                x, y = randint(0, 8), randint(0, 8)
            bool_grid[x][y] = 1
            self.grid[x][y] = "."
            self.delete -= 1
