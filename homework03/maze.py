from __future__ import annotations

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
    x, y = coord
    if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
        grid[x][y] = " "
    return grid


def _pick_exit(grid: Grid) -> Coord:
    """
    Pick a border cell that has an adjacent inner cell with a free space " ".
    This makes sure the exit is reachable.
    """
    rows, cols = len(grid), len(grid[0])
    candidates: List[Coord] = []

    # top row: neighbor is (1, j)
    for j in range(cols):
        if rows > 1 and grid[1][j] == " ":
            candidates.append((0, j))

    # bottom row: neighbor is (rows-2, j)
    for j in range(cols):
        if rows > 1 and grid[rows - 2][j] == " ":
            candidates.append((rows - 1, j))

    # left col: neighbor is (i, 1)
    for i in range(rows):
        if cols > 1 and grid[i][1] == " ":
            candidates.append((i, 0))

    # right col: neighbor is (i, cols-2)
    for i in range(rows):
        if cols > 1 and grid[i][cols - 2] == " ":
            candidates.append((i, cols - 1))

    if not candidates:
        # fallback: just any border cell
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
    """
    Binary Tree maze generation:
    carve rooms at odd/odd, then for each room carve one wall either up or right.
    """
    grid = create_grid(rows, cols)

    empty_cells: List[Coord] = []
    for x in range(rows):
        for y in range(cols):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    for x, y in empty_cells:
        candidates: List[Coord] = []

        # carve UP: needs a room at (x-2, y) which is inside the inner area
        if x - 2 >= 1 and grid[x - 2][y] == " ":
            candidates.append((x - 1, y))

        # carve RIGHT: needs a room at (x, y+2) which is inside the inner area
        if y + 2 <= cols - 2 and grid[x][y + 2] == " ":
            candidates.append((x, y + 1))

        if candidates:
            remove_wall(grid, choice(candidates))

    # exits
    if random_exit:
        start = _pick_exit(grid)
        end = _pick_exit(grid)
        # make sure they differ
        tries = 0
        while end == start and tries < 50:
            end = _pick_exit(grid)
            tries += 1
    else:
        start = (0, cols - 2)
        end = (rows - 1, 1)

    grid[start[0]][start[1]] = "X"
    grid[end[0]][end[1]] = "X"
    return grid


def get_exits(grid: Grid) -> List[Coord]:
    exits: List[Coord] = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "X":
                exits.append((i, j))
    return exits


def make_step(grid: Grid, k: int) -> Grid:
    rows, cols = len(grid), len(grid[0])
    new_grid = deepcopy(grid)

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == k:
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < rows and 0 <= nj < cols and grid[ni][nj] == " ":
                        new_grid[ni][nj] = k + 1
    return new_grid


def shortest_path(grid: Grid, exit_coord: Coord) -> Optional[List[Coord]]:
    rows, cols = len(grid), len(grid[0])

    start_pos: Optional[Tuple[int, int]] = None
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 0:
                start_pos = (i, j)
                break
        if start_pos is not None:
            break

    if start_pos is None:
        return None

    ex, ey = exit_coord

    curr: Optional[Tuple[int, int]] = None
    curr_val: Optional[int] = None

    # choose the smallest integer neighbor of the exit
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ni, nj = ex + di, ey + dj
        if 0 <= ni < rows and 0 <= nj < cols:
            v = grid[ni][nj]
            if isinstance(v, int):
                if curr_val is None or v < curr_val:
                    curr_val = v
                    curr = (ni, nj)

    if curr is None:
        return None

    path: List[Coord] = [exit_coord, curr]

    while curr != start_pos:
        i, j = curr
        cell = grid[i][j]
        if not isinstance(cell, int):
            return None

        target_val = cell - 1
        next_cell: Optional[Tuple[int, int]] = None

        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < rows and 0 <= nj < cols and grid[ni][nj] == target_val:
                next_cell = (ni, nj)
                break

        if next_cell is None:
            return None

        curr = next_cell
        path.append(curr)

    path.reverse()
    return path


def encircled_exit(grid: Grid, coord: Coord) -> bool:
    """
    True if exit has no adjacent free cell.
    """
    x, y = coord
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + di, y + dj
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == " ":
            return False
    return True


def solve_maze(grid: Grid) -> Tuple[Grid, Optional[List[Coord]]]:
    work = deepcopy(grid)
    exits = get_exits(work)
    if len(exits) < 2:
        return work, None

    start_node, end_node = exits[0], exits[1]

    # if start is encircled, swap (sometimes random exits)
    if encircled_exit(work, start_node) and not encircled_exit(work, end_node):
        start_node, end_node = end_node, start_node

    work[start_node[0]][start_node[1]] = 0

    max_steps = len(work) * len(work[0])
    for k in range(max_steps):
        new_work = make_step(work, k)
        if new_work == work:
            break
        work = new_work

        ex, ey = end_node
        reached = False
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = ex + di, ey + dj
            if (
                0 <= ni < len(work)
                and 0 <= nj < len(work[0])
                and isinstance(work[ni][nj], int)
            ):
                reached = True
                break

        if reached:
            path = shortest_path(work, end_node)
            return work, path

    return work, None


def add_path_to_grid(grid: Grid, path: Optional[List[Coord]]) -> Grid:
    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    grid_ = bin_tree_maze(15, 15)
    print(pd.DataFrame(grid_))
    _, path_ = solve_maze(grid_)
    maze_ = add_path_to_grid(grid_, path_)
    print(pd.DataFrame(maze_))
