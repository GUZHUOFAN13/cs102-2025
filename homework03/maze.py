from __future__ import annotations

from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

Cell = Union[str, int]
Grid = List[List[Cell]]
Coord = Tuple[int, int]

WALL = "■"
EMPTY = " "
EXIT = "X"


def create_grid(rows: int = 15, cols: int = 15) -> Grid:
    return [[WALL] * cols for _ in range(rows)]


def remove_wall(grid: Grid, coord: Coord) -> Grid:
    x, y = coord
    if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
        grid[x][y] = EMPTY
    return grid


def _pick_exit(grid: Grid) -> Coord:
    rows, cols = len(grid), len(grid[0])
    candidates: List[Coord] = []
    for j in range(cols):
        if rows > 1 and grid[1][j] == EMPTY:
            candidates.append((0, j))
        if rows > 1 and grid[rows - 2][j] == EMPTY:
            candidates.append((rows - 1, j))
    for i in range(rows):
        if cols > 1 and grid[i][1] == EMPTY:
            candidates.append((i, 0))
        if cols > 1 and grid[i][cols - 2] == EMPTY:
            candidates.append((i, cols - 1))

    if not candidates:
        side = randint(0, 3)
        if side == 0:
            return 0, randint(0, cols - 1)
        if side == 1:
            return rows - 1, randint(0, cols - 1)
        if side == 2:
            return randint(0, rows - 1), 0
        return randint(0, rows - 1), cols - 1
    return choice(candidates)


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> Grid:
    grid = create_grid(rows, cols)
    for x in range(1, rows, 2):
        for y in range(1, cols, 2):
            grid[x][y] = EMPTY

    for x in range(1, rows, 2):
        for y in range(1, cols, 2):
            candidates = []
            if x > 1:
                candidates.append((x - 1, y))
            if y > 1:
                candidates.append((x, y - 1))
            if candidates:
                target = choice(candidates)
                grid[target[0]][target[1]] = EMPTY

    if random_exit:
        start, end = _pick_exit(grid), _pick_exit(grid)
        tries = 0
        while end == start and tries < 50:
            end = _pick_exit(grid)
            tries += 1
    else:
        start, end = (0, cols - 2), (rows - 1, 1)

    grid[start[0]][start[1]] = EXIT
    grid[end[0]][end[1]] = EXIT
    return grid


def get_exits(grid: Grid) -> List[Coord]:
    exits = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == EXIT:
                exits.append((i, j))
    return exits


def make_step(grid: Grid, k: int) -> Grid:
    rows, cols = len(grid), len(grid[0])
    new_grid = deepcopy(grid)
    for i in range(rows):
        for j in range(cols):
            cell = grid[i][j]
            # 修复 mypy: 显式检查是否为 int 再比较
            if isinstance(cell, int) and cell == k:
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < rows and 0 <= nj < cols:
                        if new_grid[ni][nj] == EMPTY or new_grid[ni][nj] == EXIT:
                            new_grid[ni][nj] = k + 1
    return new_grid


def shortest_path(grid: Grid, exit_coord: Coord) -> Optional[List[Coord]]:
    rows, cols = len(grid), len(grid[0])
    ex, ey = exit_coord
    exit_val = grid[ex][ey]

    # 修复 mypy: 确保出口处是已经标记过的数字
    if not isinstance(exit_val, int):
        return None

    path = [exit_coord]
    curr_val: int = exit_val
    curr_pos = exit_coord

    while curr_val > 0:
        found = False
        i, j = curr_pos
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < rows and 0 <= nj < cols:
                neighbor_val = grid[ni][nj]
                # 修复 mypy: 确保邻居是 int 再做减法比较
                if isinstance(neighbor_val, int) and neighbor_val == curr_val - 1:
                    curr_pos = (ni, nj)
                    curr_val = neighbor_val
                    path.append(curr_pos)
                    found = True
                    break
        if not found:
            break

    path.reverse()
    return path


def encircled_exit(grid: Grid, coord: Coord) -> bool:
    x, y = coord
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + di, y + dj
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
            if grid[nx][ny] != WALL:
                return False
    return True


def solve_maze(grid: Grid) -> Tuple[Grid, Optional[List[Coord]]]:
    work = deepcopy(grid)
    exits = get_exits(work)
    if len(exits) < 2:
        return work, None

    start_node, end_node = exits[0], exits[1]
    work[start_node[0]][start_node[1]] = 0

    for k in range(len(work) * len(work[0])):
        new_work = make_step(work, k)
        if new_work == work:
            break
        work = new_work
        if isinstance(work[end_node[0]][end_node[1]], int):
            return work, shortest_path(work, end_node)

    return work, None


def add_path_to_grid(grid: Grid, path: Optional[List[Coord]]) -> Grid:
    if not path:
        return grid
    for i, j in path:
        cell = grid[i][j]
        if cell == EMPTY or isinstance(cell, int):
            grid[i][j] = EXIT
    return grid