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
    rows, cols = len(grid), len(grid[0])
    if 0 <= x < rows and 0 <= y < cols:
        grid[x][y] = " "
    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> Grid:
    grid = create_grid(rows, cols)

    empty_cells: List[Coord] = []
    for x in range(rows):
        for y in range(cols):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    for x, y in empty_cells:
        direction = choice(["up", "right"])
        can_go_up = x > 1
        can_go_right = y < cols - 2

        if direction == "up":
            if can_go_up:
                grid[x - 1][y] = " "
            elif can_go_right:
                grid[x][y + 1] = " "
        elif direction == "right":
            if can_go_right:
                grid[x][y + 1] = " "
            elif can_go_up:
                grid[x - 1][y] = " "

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

    start_pos: Optional[Coord] = None
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

    curr: Optional[Coord] = None
    curr_val: Optional[int] = None
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ni, nj = ex + di, ey + dj
        if 0 <= ni < rows and 0 <= nj < cols:
            cell_val = grid[ni][nj]
            if isinstance(cell_val, int):
                if curr_val is None or cell_val < curr_val:
                    curr_val = cell_val
                    curr = (ni, nj)

    if curr is None:
        return None

    path: List[Coord] = [exit_coord, curr]

    while curr != start_pos:
        i, j = curr
        val = grid[i][j]
        if not isinstance(val, int):
            return None

        target_val = val - 1
        next_cell: Optional[Coord] = None

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
            if 0 <= ni < len(work) and 0 <= nj < len(work[0]) and isinstance(work[ni][nj], int):
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
