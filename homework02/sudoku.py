import pathlib
import random
import typing as tp

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """Прочитать Судоку из указанного файла"""
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку"""
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print("".join(grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)))
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """Сгруппировать значения values в список, состоящий из списков по n элементов"""
    return [values[i : i + n] for i in range(0, len(values), n)]


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos"""
    r, _ = pos
    return list(grid[r])


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos"""
    _, c = pos
    return [grid[r][c] for r in range(len(grid))]


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos"""
    r, c = pos
    br, bc = (r // 3) * 3, (c // 3) * 3
    return [grid[rr][cc] for rr in range(br, br + 3) for cc in range(bc, bc + 3)]


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти первую свободную позицию в пазле"""
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == ".":
                return (r, c)
    return None


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции"""
    r, c = pos
    if grid[r][c] != ".":
        return set()
    used = set(get_row(grid, pos)) | set(get_col(grid, pos)) | set(get_block(grid, pos))
    used.discard(".")
    return set("123456789") - used


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """Решение пазла, заданного в grid"""
    g = [row[:] for row in grid]

    def backtrack() -> bool:
        empty = find_empty_positions(g)
        if empty is None:
            return True
        r, c = empty
        for v in sorted(list(find_possible_values(g, (r, c)))):
            g[r][c] = v
            if backtrack():
                return True
            g[r][c] = "."
        return False

    return g if backtrack() else None


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """Если решение solution верно, то вернуть True, в противном случае False"""
    if not solution:
        return False
    need = set("123456789")
    for r in range(9):
        if set(solution[r]) != need:
            return False
    for c in range(9):
        if set(solution[r][c] for r in range(9)) != need:
            return False
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            if set(solution[r][c] for r in range(br, br + 3) for c in range(bc, bc + 3)) != need:
                return False
    return True


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов"""
    N = max(0, min(81, N))
    full = [["." for _ in range(9)] for _ in range(9)]

    def fill_backtrack() -> bool:
        empty = find_empty_positions(full)
        if empty is None:
            return True
        r, c = empty
        candidates = list(find_possible_values(full, (r, c)))
        random.shuffle(candidates)
        for v in candidates:
            full[r][c] = v
            if fill_backtrack():
                return True
            full[r][c] = "."
        return False

    fill_backtrack()
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    keep = set(cells[:N])
    puzzle = [[full[r][c] if (r, c) in keep else "." for c in range(9)] for r in range(9)]
    return puzzle


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        try:
            grid = read_sudoku(fname)
            display(grid)
            solution = solve(grid)
            if not solution:
                print(f"Puzzle {fname} can't be solved")
            else:
                display(solution)
        except FileNotFoundError:
            print(f"Warning: {fname} not found.")
