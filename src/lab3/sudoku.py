import pathlib
import time
import typing as tp
from copy import deepcopy

from src.lab3.gen import Sudoku

T = tp.TypeVar("T")


def run_solve(filename: str) -> None:
    grid = read_sudoku(filename)
    start = time.time()
    solve(grid)
    end = time.time()
    print(f"{filename}: {end - start:.3f}s")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """Прочитать Судоку из указанного файла"""
    p = pathlib.Path(path)
    with p.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    return group(digits, 9)


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку"""
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for r in range(9):
        print("".join(grid[r][c].center(width) + ("|" if c in (2, 5) else "") for c in range(9)))
        if r in (2, 5):
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать values в списки по n элементов.
    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    if len(values) % n != 0:
        raise ValueError("Values count must be multiple of n")
    # Явная аннотация, чтобы mypy не ругался
    sudoku_matrix: tp.List[tp.List[T]] = [values[i : i + n] for i in range(0, len(values), n)]
    return sudoku_matrix


def _check_pos(pos: tp.Tuple[int, int]) -> None:
    r, c = pos
    if not (0 <= r < 9 and 0 <= c < 9):
        raise ValueError("Pos value wrong")


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Все значения строки pos[0]"""
    _check_pos(pos)
    return grid[pos[0]]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Все значения столбца pos[1]"""
    _check_pos(pos)
    return [row[pos[1]] for row in grid]


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Все значения 3×3 блока, содержащего pos"""
    _check_pos(pos)
    r0 = (pos[0] // 3) * 3
    c0 = (pos[1] // 3) * 3
    return [grid[r][c] for r in range(r0, r0 + 3) for c in range(c0, c0 + 3)]


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти первую свободную позицию ('.'). Если нет — вернуть None."""
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == ".":
                return (i, j)
    return None


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """Вернуть множество возможных значений для позиции pos"""
    possible = [True] * 10
    possible[0] = False

    for v in get_block(grid, pos):
        if v != ".":
            possible[int(v)] = False
    for v in get_col(grid, pos):
        if v != ".":
            possible[int(v)] = False
    for v in get_row(grid, pos):
        if v != ".":
            possible[int(v)] = False

    return {str(i) for i in range(1, 10) if possible[i]}


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """Решение судоку (бэктрекинг). Возвращает решённую матрицу или None."""
    pos = find_empty_positions(grid)
    if pos is None:
        return grid  # уже решено

    values = find_possible_values(grid, pos)
    if not values:
        return None

    r, c = pos
    for val in values:
        new_grid = deepcopy(grid)  # важно — не портим исходный
        new_grid[r][c] = val
        solution = solve(new_grid)
        if solution is not None:
            return solution

    return None


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """Если решение корректно — True, иначе False"""
    # строки
    for i in range(9):
        row = get_row(solution, (i, 0))
        if len(set(row)) != 9 or "." in row:
            return False
    # столбцы
    for j in range(9):
        col = get_col(solution, (0, j))
        if len(set(col)) != 9 or "." in col:
            return False
    # блоки 3x3
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            block = get_block(solution, (i, j))
            if len(set(block)) != 9 or "." in block:
                return False
    # нет пустых позиций
    return find_empty_positions(solution) is None


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку, заполненного на N элементов"""
    sudoku_manager = Sudoku(N)
    sudoku_manager.mix()
    sudoku_manager.delete_cells()
    return sudoku_manager.grid


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        g = read_sudoku(fname)
        display(g)
        sol = solve(g)
        if sol is None:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(sol)
