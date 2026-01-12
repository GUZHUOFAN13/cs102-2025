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


def _pick_exit(grid: Grid) -> Coord:
    """选择一个可通行的边界点作为出口"""
    rows, cols = len(grid), len(grid[0])
    candidates: List[Coord] = []

    for j in range(cols):
        if grid[1][j] == " ":
            candidates.append((0, j))
        if grid[rows - 2][j] == " ":
            candidates.append((rows - 1, j))

    for i in range(rows):
        if grid[i][1] == " ":
            candidates.append((i, 0))
        if grid[i][cols - 2] == " ":
            candidates.append((i, cols - 1))

    return choice(candidates) if candidates else (0, 0)


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> Grid:
    grid = create_grid(rows, cols)
    for i in range(1, rows, 2):
        for j in range(1, cols, 2):
            grid[i][j] = " "
            neighbors = []
            if i > 1:
                neighbors.append((i - 1, j))
            if j > 1:
                neighbors.append((i, j - 1))
            if neighbors:
                remove_wall(grid, choice(neighbors))
    if random_exit:
        ex = _pick_exit(grid)
        grid[ex[0]][ex[1]] = "X"
    return grid


def make_step(grid: Grid, step: int) -> Grid:
    new_grid = deepcopy(grid)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == step:
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < len(grid) and 0 <= nj < len(grid[i]) and grid[ni][nj] == " ":
                        new_grid[ni][nj] = step + 1
    return new_grid


def shortest_path(grid: Grid, exit_coord: Coord) -> Optional[List[Coord]]:
    ex, ey = exit_coord
    if isinstance(grid[ex][ey], int):
        curr = (ex, ey)
        path: List[Coord] = [curr]
    else:
        best: Optional[Coord] = None
        best_val: Optional[int] = None
        for di, dj in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            ni, nj = ex + di, ey + dj
            if 0 <= ni < len(grid) and 0 <= nj < len(grid[0]) and isinstance(grid[ni][nj], int):
                v = grid[ni][nj]
                if best_val is None or v < best_val:
                    best_val = v
                    best = (ni, nj)
        if best is None:
            return None
        curr = best
        path = [curr]

    while True:
        i, j = curr
        val = grid[i][j]
        if val == 0:
            break
        found = False
        for di, dj in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            ni, nj = i + di, j + dj
            if (
                0 <= ni < len(grid)
                and 0 <= nj < len(grid[0])
                and isinstance(grid[ni][nj], int)
                and grid[ni][nj] == val - 1
            ):
                curr = (ni, nj)
                path.append(curr)
                found = True
                break
        if not found:
            return None
    return path


def solve_maze(grid: Grid) -> Tuple[Grid, Optional[List[Coord]]]:
    work = deepcopy(grid)
    max_steps = len(work) * len(work[0])

    for i in range(len(work)):
        for j in range(len(work[i])):
            if work[i][j] == "X":
                end_node = (i, j)
            if work[i][j] == " " and (i == 0 or j == 0 or i == len(work) - 1 or j == len(work[i]) - 1):
                work[i][j] = 0

    for k in range(max_steps):
        new_work = make_step(work, k)
        if new_work == work:
            break
        work = new_work

    ex, ey = end_node
    reached = False
    for di, dj in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
        ni, nj = ex + di, ey + dj
        if 0 <= ni < len(work) and 0 <= nj < len(work[0]) and isinstance(work[ni][nj], int):
            reached = True
            break

    if reached:
        path = shortest_path(work, end_node)
        if path:
            path.reverse()  # ✅ 反转方向
        return work, path
    return work, None


def add_path_to_grid(grid: Grid, path: Optional[List[Coord]]) -> Grid:
    if not path:
        return grid
    new_grid = deepcopy(grid)
    for i, j in path:
        if new_grid[i][j] == " ":
            new_grid[i][j] = "."
    return new_grid
