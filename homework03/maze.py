from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

Cell = Union[str, int]
Grid = List[List[Cell]]
Coord = Tuple[int, int]


def create_grid(rows: int = 15, cols: int = 15) -> Grid:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: Grid, coord: Coord) -> Grid:
    x, y = coord
    if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
        grid[x][y] = " "
    return grid



def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> Grid:
    grid = create_grid(rows, cols)

    # делаем "комнаты" в нечётных клетках
    empty_cells: List[Coord] = []
    for x in range(rows):
        for y in range(cols):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    # бинарное дерево: соединяем комнату либо вверх, либо вправо
    for x, y in empty_cells:
        direction = choice(["up", "right"])
        can_go_up = x > 1
        can_go_right = y < cols - 2

        if direction == "up":
            if can_go_up:
                grid[x - 1][y] = " "
            elif can_go_right:
                grid[x][y + 1] = " "
        else:
            if can_go_right:
                grid[x][y + 1] = " "
            elif can_go_up:
                grid[x - 1][y] = " "

    # вход и выход
    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in] = "X"
    grid[x_out][y_out] = "X"
    return grid


def get_exits(grid: Grid) -> List[Coord]:
    exits: List[Coord] = []
    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if cell == "X":
                exits.append((x, y))
    return exits


def make_step(grid: Grid, k: int) -> Grid:
    """
    Волновой шаг: все клетки со значением k расширяют фронт на соседние нули.
    grid меняется "на месте" (как у тебя), и возвращается для удобства.
    """
    rows, cols = len(grid), len(grid[0])

    # соберём координаты всех k (чтобы новые k+1 не влияли на текущий проход)
    frontier: List[Coord] = []
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == k:
                frontier.append((i, j))

    # 4-соседство
    for i, j in frontier:
        for di, dj in [(-1, 0), (0, -1), (1, 0), (0, 1)]:  # фиксированный порядок
            ni, nj = i + di, j + dj
            if 0 <= ni < rows and 0 <= nj < cols and grid[ni][nj] == 0:
                grid[ni][nj] = k + 1

    return grid


def shortest_path(grid: Grid, exit_coord: Coord) -> Optional[List[Coord]]:
    """
    Восстанавливает кратчайший путь по числам: от выхода к старту (к 1).
    Поддерживает, что клетка выхода может быть 'X' или 0 (тогда берём соседнюю цифру).
    Возвращает список координат (включая выход), или None если пути нет.
    """
    rows, cols = len(grid), len(grid[0])
    ex, ey = exit_coord

    if not (0 <= ex < rows and 0 <= ey < cols):
        return None

    path: List[Coord] = [exit_coord]

    # определяем стартовую точку обратного хода: либо сама клетка (если int>0),
    # либо лучший сосед-цифра
    cur: Coord
    cur_val: int

    cell = grid[ex][ey]
    if isinstance(cell, int) and cell > 0:
        cur = (ex, ey)
        cur_val = cell
    else:
        candidates: List[Tuple[int, Coord]] = []
        for di, dj in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            ni, nj = ex + di, ey + dj
            if 0 <= ni < rows and 0 <= nj < cols:
                cell = grid[ni][nj]
                if isinstance(cell, int) and cell > 0:
                 candidates.append((cell, (ni, nj)))

        if not candidates:
            return None
        candidates.sort(key=lambda t: t[0])
        cur_val, cur = candidates[0]
        path.append(cur)

    # теперь идём по убыванию до 1
    while cur_val > 1:
        next_coord: Optional[Coord] = None
        want = cur_val - 1

        for di, dj in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            ni, nj = cur[0] + di, cur[1] + dj
            if 0 <= ni < rows and 0 <= nj < cols and grid[ni][nj] == want:
                next_coord = (ni, nj)
                break

        if next_coord is None:
            return None

        path.append(next_coord)
        cur = next_coord
        cur_val = want

    return path


def encircled_exit(grid: Grid, coord: Coord) -> bool:
    """
    Выход считается "окружённым", если рядом нет ни одной клетки с пробелом ' '.
    (Раньше углы всегда True — это ломает корректные случаи.)
    """
    x, y = coord
    rows, cols = len(grid), len(grid[0])

    for di, dj in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
        ni, nj = x + di, y + dj
        if 0 <= ni < rows and 0 <= nj < cols and grid[ni][nj] == " ":
            return False
    return True


def solve_maze(grid: Grid) -> Tuple[Grid, Optional[List[Coord]]]:
    exits = get_exits(grid)
    if len(exits) != 2:
        return grid, None

    # если какой-то выход реально закрыт стенами — нет решения
    for e in exits:
        if encircled_exit(grid, e):
            return grid, None

    start_coord, end_coord = exits

    # создаём "числовую" копию: пробелы -> 0, стены остаются '■'
    work = deepcopy(grid)
    rows, cols = len(work), len(work[0])

    for r in range(rows):
        for c in range(cols):
            if work[r][c] == " ":
                work[r][c] = 0

    # выходы считаем проходимыми
    work[start_coord[0]][start_coord[1]] = 0
    work[end_coord[0]][end_coord[1]] = 0

    # стартовая точка волны
    work[start_coord[0]][start_coord[1]] = 1

    # максимум шагов (чтобы не зациклиться)
    max_steps = rows * cols
    k = 1
    while work[end_coord[0]][end_coord[1]] == 0 and k <= max_steps:
        prev = deepcopy(work)
        make_step(work, k)
        if work == prev:
            return work, None
        k += 1

    if not isinstance(work[end_coord[0]][end_coord[1]], int) or work[end_coord[0]][end_coord[1]] == 0:
        return work, None

    # shortest_path даёт "от выхода к старту"
    path_back = shortest_path(work, end_coord)
    if path_back is None:
        return work, None

    # solve_maze обычно ждут "от старта к выходу"
    path = list(reversed(path_back))
    return work, path


def add_path_to_grid(grid: Grid, path: Optional[List[Coord]]) -> Grid:
    """
    Рисует путь символом 'X' на копии лабиринта.
    """
    new_grid = deepcopy(grid)
    if not path:
        return new_grid

    for x, y in path:
        if 0 <= x < len(new_grid) and 0 <= y < len(new_grid[0]):
            new_grid[x][y] = "X"
    return new_grid


if __name__ == "__main__":
    g = bin_tree_maze(15, 15)
    solved, p = solve_maze(g)
    painted = add_path_to_grid(g, p)

    # простой вывод без pandas (чтобы не требовать пакет)
    for row in painted:
        print("".join(str(x) if x != 0 else " " for x in row))
