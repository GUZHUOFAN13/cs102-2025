from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(
    grid: List[List[Union[str, int]]], coord: Tuple[int, int]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """
    x, y = coord
    if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
        grid[x][y] = " "
    return grid


def bin_tree_maze(
    rows: int = 15, cols: int = 15, random_exit: bool = True
) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    for i in range(len(empty_cells)):
        x, y = empty_cells[i]
        possible = []
        if x > 1:
            possible.append("up")
        if y < cols - 2:
            possible.append("right")

        if len(possible) > 0:
            move = choice(possible)
            if move == "up":
                grid[x - 1][y] = " "
            else:
                grid[x][y + 1] = " "

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
    """

    :param grid:
    :return:
    """
    result = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == "X":
                result.append((r, c))
    return result


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """
    rows = len(grid)
    cols = len(grid[0])
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == k:
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if grid[nr][nc] == " " or grid[nr][nc] == "X":
                            grid[nr][nc] = k + 1
    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[List[Tuple[int, int]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """
    r, c = exit_coord
    if not isinstance(grid[r][c], int):
        return None

    path = [exit_coord]
    curr_r, curr_c = r, c
    curr_val = grid[r][c]

    while curr_val > 1:
        found = False
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = curr_r + dr, curr_c + dc
            if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
                val = grid[nr][nc]
                if isinstance(val, int) and val == curr_val - 1:
                    curr_r, curr_c = nr, nc
                    curr_val = val
                    path.append((nr, nc))
                    found = True
                    break
        if not found:
            break

    path.reverse()
    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """
    r, c = coord
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]):
            if grid[nr][nc] != "■":
                return False
    return True


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[List[Tuple[int, int]]]]:
    """

    :param grid:
    :return:
    """
    exits = get_exits(grid)
    if len(exits) < 2:
        return grid, None

    work_grid = deepcopy(grid)
    start_pos = exits[0]
    end_pos = exits[1]

    work_grid[start_pos[0]][start_pos[1]] = 1

    max_steps = len(grid) * len(grid[0])
    for k in range(1, max_steps):
        work_grid = make_step(work_grid, k)
        if isinstance(work_grid[end_pos[0]][end_pos[1]], int):
            path = shortest_path(work_grid, end_pos)
            return work_grid, path

    return work_grid, None


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[List[Tuple[int, int]]]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for r, c in path:
            grid[r][c] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))