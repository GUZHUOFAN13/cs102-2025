from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(
    grid: List[List[Union[str, int]]], coord: Tuple[int, int]
) -> List[List[Union[str, int]]]:
    x, y = coord
    if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
        grid[x][y] = " "
    return grid


def bin_tree_maze(
    rows: int = 15, cols: int = 15, random_exit: bool = True
) -> List[List[Union[str, int]]]:
    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    for x, y in empty_cells:
        candidates = []
        if x - 2 >= 0:
            candidates.append((x - 1, y))
        if y + 2 < cols:
            candidates.append((x, y + 1))

        if candidates:
            wall_coord = choice(candidates)
            remove_wall(grid, wall_coord)

    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    exits = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "X":
                exits.append((i, j))
    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
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


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    rows, cols = len(grid), len(grid[0])
    start_pos = None
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 0:
                start_pos = (i, j)
                break
        if start_pos:
            break

    if not start_pos:
        return None

    ex, ey = exit_coord
    curr = None
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ni, nj = ex + di, ey + dj
        if 0 <= ni < rows and 0 <= nj < cols and isinstance(grid[ni][nj], int):
            curr = (ni, nj)
            break

    if not curr:
        return None

    path = [exit_coord, curr]
    while curr != start_pos:
        i, j = curr
        target_val = grid[i][j] - 1
        found_next = False
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < rows and 0 <= nj < cols and grid[ni][nj] == target_val:
                curr = (ni, nj)
                path.append(curr)
                found_next = True
                break
        if not found_next:
            return None

    path.reverse()
    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    x, y = coord
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + di, y + dj
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
            if grid[nx][ny] == " ":
                return False
    return True


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[
    List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
]:
    work = deepcopy(grid)
    exits = get_exits(work)
    if len(exits) < 2:
        return work, None

    start_node, end_node = exits[0], exits[1]
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


def add_path_to_grid(
    grid: List[List[Union[str, int]]],
    path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]],
) -> List[List[Union[str, int]]]:
    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
