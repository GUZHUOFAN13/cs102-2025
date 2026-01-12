from __future__ import annotations

from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

Cell = Union[str, int]
Grid = List[List[Cell]]
Coord = Tuple[int, int]


def create_grid(rows: int = 15, cols: int = 15) -> Grid:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: Grid, coord: Coord) -> Grid:
    """
    Remove wall at coord if coord is inside the grid.
    IMPORTANT (tests): must NOT create a new grid; should mutate and return the same grid.
    """
    x, y = coord
    if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
        grid[x][y] = " "
    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> Grid:
    """
    Binary Tree maze:
    - carve cells at odd/odd
    - from each carved cell carve one wall either UP or RIGHT (if possible)
    - put two exits 'X' on the border
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
        if x - 2 >= 0:
            candidates.append((x - 1, y))  # wall up
        if y + 2 < cols:
            candidates.append((x, y + 1))  # wall right
        if candidates:
            remove_wall(grid, choice(candidates))

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
    """
    Wave expansion from cells == k into free spaces " ".
    IMPORTANT (tests): must not modify input grid in-place; return new grid.
    """
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


def encircled_exit(grid: Grid, coord: Coord) -> bool:
    """
    Exit is encircled if all valid adjacent cells are NOT free space " ".
    IMPORTANT (tests): only " " counts as passable (not "X", not ints).
    """
    x, y = coord
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + di, y + dj
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == " ":
            return False
    return True


def shortest_path(grid: Grid, exit_coord: Coord) -> Optional[List[Coord]]:
    """
    Restore shortest path from start (cell == 0) to the given exit (cell == "X")
    using the numbered wave in grid.

    IMPORTANT (tests):
    - If exit_coord is not actually an "X" in grid -> return None
    - Return a list of coords INCLUDING start and INCLUDING the exit as the last element.
    """
    rows, cols = len(grid), len(grid[0])
    ex, ey = exit_coord

    if not (0 <= ex < rows and 0 <= ey < cols):
        return None
    if grid[ex][ey] != "X":
        return None

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

    # Find an integer neighbor of exit (the wave reaches a cell adjacent to the exit)
    curr: Optional[Coord] = None
    curr_val: Optional[int] = None
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

    # Backtrack down to 0
    path: List[Coord] = [curr]
    while curr != start_pos:
        i, j = curr
        cell = grid[i][j]
        if not isinstance(cell, int):
            return None
        target = cell - 1

        nxt: Optional[Coord] = None
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < rows and 0 <= nj < cols and grid[ni][nj] == target:
                nxt = (ni, nj)
                break

        if nxt is None:
            return None

        curr = nxt
        path.append(curr)

    path.reverse()  # now from start to neighbor
    path.append(exit_coord)  # exit as the last element
    return path


def solve_maze(grid: Grid) -> Tuple[Grid, Optional[List[Coord]]]:
    """
    Solve maze using wave algorithm:
    - pick exits[0] as start, exits[1] as end (DO NOT swap, tests rely on this)
    - start cell becomes 0
    - expand wave into " "
    - if end has an integer neighbor -> restore path
    """
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
            if 0 <= ni < len(work) and 0 <= nj < len(work[0]) and isinstance(work[ni][nj], int):
                reached = True
                break

        if reached:
            path = shortest_path(work, end_node)
            return work, path

    return work, None


def add_path_to_grid(grid: Grid, path: Optional[List[Coord]]) -> Grid:
    """
    Mark the found path on the grid using "X".
    """
    if path:
        for i, j in path:
            if 0 <= i < len(grid) and 0 <= j < len(grid[0]):
                grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    # Optional local demo without requiring pandas in CI/tests.
    grid_ = bin_tree_maze(15, 15)
    solved_grid, path_ = solve_maze(grid_)
    add_path_to_grid(grid_, path_)
    # Simple print
    for row in grid_:
        print("".join(str(c) for c in row))
