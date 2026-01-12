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

    rooms: List[Coord] = []
    for x in range(rows):
        for y in range(cols):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = EMPTY
                rooms.append((x, y))

    for x, y in rooms:
        candidates: List[Coord] = []
        if x - 2 >= 1 and grid[x - 2][y] == EMPTY:
            candidates.append((x - 1, y))
        if y + 2 <= cols - 2 and grid[x][y + 2] == EMPTY:
            candidates.append((x, y + 1))
        if candidates:
            remove_wall(grid, choice(candidates))

    if random_exit:
        start = _pick_exit(grid)
        end = _pick_exit(grid)
        tries = 0
        while end == start and tries < 50:
            end = _pick_exit(grid)
            tries += 1
    else:
        start = (0, cols - 2)
        end = (rows - 1, 1)

    grid[start[0]][start[1]] = EXIT
    grid[end[0]][end[1]] = EXIT
    return grid


def get_exits(grid: Grid) -> List[Coord]:
    exits: List[Coord] = []
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
            if grid[i][j] == k:
                for di, dj in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < rows and 0 <= nj < cols and new_grid[ni][nj] == EMPTY:
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

    # 情况1：出口格本身已经是数字（有人会把出口也标号）
    if isinstance(grid[ex][ey], int):
        curr = (ex, ey)
        path: List[Coord] = [curr]
    else:
        # 情况2：出口格是 "X"，从它的邻居里找最小的数字作为回溯起点
        best: Optional[Coord] = None
        best_val: Optional[int] = None

        for di, dj in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            ni, nj = ex + di, ey + dj
            if 0 <= ni < rows and 0 <= nj < cols:
                cell = grid[ni][nj]
                if isinstance(cell, int):
                    v: int = cell
                    if best_val is None or v < best_val:
                        best_val = v
                        best = (ni, nj)

        if best is None:
            return None

        curr = best
        path = [exit_coord, curr]

    # 回溯：每次找 value-1 的邻居（固定方向顺序保证测试一致）
    while curr != start_pos:
        i, j = curr
        cell = grid[i][j]
        if not isinstance(cell, int):
            return None

        target = cell - 1
        nxt: Optional[Coord] = None
        for di, dj in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < rows and 0 <= nj < cols and grid[ni][nj] == target:
                nxt = (ni, nj)
                break

        if nxt is None:
            return None

        curr = nxt
        path.append(curr)

    path.reverse()
    return path


def encircled_exit(grid: Grid, coord: Coord) -> bool:
    x, y = coord
    for di, dj in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
        nx, ny = x + di, y + dj
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
            # 只要旁边不是墙，就说明没被围住（空格/数字/出口都算通）
            if grid[nx][ny] != WALL:
                return False
    return True


def solve_maze(grid: Grid) -> Tuple[Grid, Optional[List[Coord]]]:
    work = deepcopy(grid)
    exits = get_exits(work)
    if len(exits) < 2:
        return work, None

    start_node, end_node = exits[0], exits[1]

    # 起点出口标 0
    work[start_node[0]][start_node[1]] = 0

    max_steps = len(work) * len(work[0])
    for k in range(max_steps):
        new_work = make_step(work, k)
        if new_work == work:
            break
        work = new_work

        # 到达判定：end_node 周围出现数字（表示波前到达出口旁）
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
                path.reverse()
            return work, path

    return work, None


def add_path_to_grid(grid: Grid, path: Optional[List[Coord]]) -> Grid:
    if not path:
        return grid
    # 不覆盖墙/出口，只把路径内部标出来（如果你作业要求别的符号，可改这里）
    for i, j in path:
        if grid[i][j] == EMPTY:
            grid[i][j] = EXIT
    return grid
