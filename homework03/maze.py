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
    directions = ["up", "right"]
    x, y = coord
    rows, cols = len(grid), len(grid[0])

    direction = choice(directions)
    if direction == "up":
        if 0 <= x - 2 < rows and 0 <= y < cols:
            grid[x - 1][y] = " "
        else:
            direction = "right"

    if direction == "right":
        if 0 <= x < rows and 0 <= y + 2 < cols:
            grid[x][y + 1] = " "
        elif 0 <= x - 2 < rows and 0 <= y < cols:
            grid[x - 1][y] = " "

    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> Grid:
    grid = create_grid(rows, cols)
    empty_cells = []
    for x in range(rows):
        for y in range(cols):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    while empty_cells:
        x, y = empty_cells.pop(0)
        remove_wall(grid, (x, y))

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
    return [(x, y) for x, row in enumerate(grid) for y, elem in enumerate(row) if elem == "X"]


def make_step(grid: Grid, k: int) -> Grid:
    all_coords = []
    rows, cols = len(grid), len(grid[0])
    for x in range(rows):
        for y in range(cols):
            if grid[x][y] == k:
                all_coords.append((x, y))

    k += 1
    for x, y in all_coords:
        possible_pos = [
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1),
        ]
        for nx, ny in possible_pos:
            if 0 <= nx < rows and 0 <= ny < cols and grid[nx][ny] == 0:
                grid[nx][ny] = k
    return grid


def shortest_path(grid: Grid, exit_coord: Coord) -> Optional[List[Coord]]:
    ex, ey = exit_coord
    # Ensure the exit cell has a numeric step value
    if not isinstance(grid[ex][ey], int):
        return None
    
    path_len = int(grid[ex][ey])
    cur_coord = exit_coord
    path = [cur_coord]
    
    rows, cols = len(grid), len(grid[0])
    k = path_len

    while k > 1:
        possible_pos = [
            (cur_coord[0] - 1, cur_coord[1]),
            (cur_coord[0] + 1, cur_coord[1]),
            (cur_coord[0], cur_coord[1] - 1),
            (cur_coord[0], cur_coord[1] + 1),
        ]
        found_next = False
        for nx, ny in possible_pos:
            if 0 <= nx < rows and 0 <= ny < cols:
                val = grid[nx][ny]
                if isinstance(val, int) and val == k - 1:
                    path.append((nx, ny))
                    cur_coord = (nx, ny)
                    k -= 1
                    found_next = True
                    break
        
        if not found_next:
            return None

    return path


def encircled_exit(grid: Grid, coord: Coord) -> bool:
    x, y = coord
    rows, cols = len(grid), len(grid[0])
    
    # Check strict corners
    if (x == 0 and y == 0) or (x == rows - 1 and y == cols - 1):
        return True
    if (x == 0 and y == cols - 1) or (x == rows - 1 and y == 0):
        return True

    # Check edges being blocked by walls
    if x == rows - 1:
        if grid[x - 1][y] != " ":
            return True
    elif x == 0:
        if grid[x + 1][y] != " ":
            return True
    elif y == cols - 1:
        if grid[x][y - 1] != " ":
            return True
    elif y == 0:
        if grid[x][y + 1] != " ":
            return True
            
    return False


def solve_maze(grid: Grid) -> Tuple[Grid, Optional[List[Coord]]]:
    exits = get_exits(grid)
    if len(exits) != 2:
        return grid, None

    entrance, exit_ = exits[0], exits[1]
    if encircled_exit(grid, entrance) or encircled_exit(grid, exit_):
        return grid, None

    # Prepare grid for Wave Algorithm (0 for spaces, 1 for start)
    k = 0
    grid[entrance[0]][entrance[1]] = 1
    
    rows, cols = len(grid), len(grid[0])
    for x in range(rows):
        for y in range(cols):
            if grid[x][y] == " " or grid[x][y] == "X":
                if (x, y) != entrance:
                    grid[x][y] = 0

    # Propagate wave
    while grid[exit_[0]][exit_[1]] == 0:
        k += 1
        prev_grid = deepcopy(grid)
        make_step(grid, k)
        if grid == prev_grid: # No progress made, path impossible
            return grid, None

    path = shortest_path(grid, exit_)
    return grid, path


def add_path_to_grid(grid: Grid, path: Optional[List[Coord]]) -> Grid:
    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
                    
        # Clean up the numbers left by the wave algorithm
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if isinstance(grid[i][j], int):
                    grid[i][j] = " "
    return grid


if __name__ == "__main__":
    grid_ = bin_tree_maze(15, 15)
    print(pd.DataFrame(grid_))
    _, path_ = solve_maze(grid_)
    maze_ = add_path_to_grid(grid_, path_)
    print(pd.DataFrame(maze_))
