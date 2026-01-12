from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd

Cell = Union[str, int]
Grid = List[List[Cell]]
Coord = Tuple[int, int]


def create_grid(rows: int = 15, cols: int = 15) -> Grid:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: Grid, coord: Coord) -> Grid:
    """
    Удаляет стену в указанной координате (делает клетку проходом).
    coord обычно — клетка-стена между двумя "комнатами" (odd-odd).
    """
    x, y = coord
    if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
        grid[x][y] = " "
    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> Grid:
    """
    Генерация лабиринта алгоритмом Binary Tree.
    Стены: '■'
    Проходы: ' '
    Вход/выход: 'X'
    """
    grid = create_grid(rows, cols)

    empty_cells: List[Coord] = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    # ---- Binary Tree carving: for each room carve either UP or RIGHT ----
    for x, y in empty_cells:
        candidates: List[Tuple[str, Coord]] = []

        # up room: (x-2, y), wall between: (x-1, y)
        if x - 2 >= 1 and grid[x - 2][y] == " ":
            candidates.append(("U", (x - 1, y)))

        # right room: (x, y+2), wall between: (x, y+1)
        if y + 2 <= cols - 2 and grid[x][y + 2] == " ":
            candidates.append(("R", (x, y + 1)))

        if candidates:
            _, wall_coord = choice(candidates)
            remove_wall(grid, wall_coord)

    # генерация входа и выхода
    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: Grid) -> List[Coord]:
    """Вернуть координаты всех выходов/входов (клетки со значением 'X')."""
    exits: List[Coord] = []
    for i, row in enumerate(grid):
        for j, val in enumerate(row):
            if val == "X":
                exits.append((i, j))
    return exits


def make_step(grid: Grid, k: int) -> Grid:
    """
    Один шаг "волны": из всех клеток со значением k
    распространиться в соседние пустые клетки " " и пометить их k+1.
    """
    rows, cols = len(grid), len(grid[0])
    new_grid = deepcopy(grid)

    for i in range(rows):
        for j in range(cols):
            if new_grid[i][j] == k:
                for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    ni, nj = i + di, j + dj
                    if 0 <= ni < rows and 0 <= nj < cols and new_grid[ni][nj] == " ":
                        new_grid[ni][nj] = k + 1

    return new_grid


def shortest_path(grid: Grid, exit_coord: Coord) -> Optional[Union[Coord, List[Coord]]]:
    """
    Восстановить кратчайший путь от старта (клетка с 0) до exit_coord (вторая 'X'),
    двигаясь по убывающим числам.
    Возвращает список координат пути (включая обе точки).
    """
    rows, cols = len(grid), len(grid[0])

    # найти старт (где стоит 0)
    start: Optional[Coord] = None
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 0:
                start = (i, j)
                break
        if start is not None:
            break
    if start is None:
        return None

    ex, ey = exit_coord

    # найти соседнюю клетку с числом (где волна подошла к выходу)
    best_neighbor: Optional[Coord] = None
    best_val: Optional[int] = None
    for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        ni, nj = ex + di, ey + dj
        if 0 <= ni < rows and 0 <= nj < cols and isinstance(grid[ni][nj], int):
            v = grid[ni][nj]
            if best_val is None or v < best_val:
                best_val = v
                best_neighbor = (ni, nj)

    if best_neighbor is None or best_val is None:
        return None

    # восстановление: выход -> ... -> старт по убывающим значениям
    path: List[Coord] = [exit_coord]
    cur = best_neighbor
    cur_val = best_val
    path.append(cur)

    while cur != start:
        i, j = cur
        next_cell: Optional[Coord] = None
        next_val = cur_val - 1

        for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            ni, nj = i + di, j + dj
            if 0 <= ni < len(work) and 0 <= nj < len(work[0]) and isinstance(work[ni][nj], int):

        if next_cell is None:
            return None

        cur = next_cell
        cur_val = next_val
        path.append(cur)

    path.reverse()
    return path


def encircled_exit(grid: Grid, coord: Coord) -> bool:
    """
    True если выход окружён стенами и из него нельзя сделать шаг в лабиринт.
    """
    rows, cols = len(grid), len(grid[0])
    x, y = coord
    for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nx, ny = x + di, y + dj
        if 0 <= nx < rows and 0 <= ny < cols:
            if grid[nx][ny] == " ":
                return False
    return True


def solve_maze(grid: Grid) -> Tuple[Grid, Optional[Union[Coord, List[Coord]]]]:
    """
    Решение волновым алгоритмом (BFS-метки).
    Возвращает (grid_with_marks, path_coords or None).
    Исходный grid НЕ меняет.
    """
    work = deepcopy(grid)
    exits = get_exits(work)
    if len(exits) < 2:
        return work, None

    start_exit, end_exit = exits[0], exits[1]

    # пометим старт как 0
    sx, sy = start_exit
    work[sx][sy] = 0

    k = 0
    while True:
        new_work = make_step(work, k)

        # волна не расширилась — пути нет
        if new_work == work:
            return work, None

        work = new_work

        # проверка: подошли ли к выходу (есть сосед с int)
        ex, ey = end_exit
        reached = False
        for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            ni, nj = ex + di, ey + dj
            if (
                0 <= ni < len(work)
                and 0 <= nj < len(work[0])
                and isinstance(work[ni][nj], int)
            ):
                reached = True
                break

        if reached:
            break

        k += 1
        if k > len(work) * len(work[0]):  # защита
            return work, None

    path = shortest_path(work, end_exit)
    return work, path


def add_path_to_grid(grid: Grid, path: Optional[Union[Coord, List[Coord]]]) -> Grid:
    """
    Рисует путь в grid символом 'X' по координатам path.
    """
    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
