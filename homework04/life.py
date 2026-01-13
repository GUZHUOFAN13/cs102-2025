import pathlib
import random
import typing as tp

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Size of the grid
        self.rows, self.cols = size
        # Previous generation
        self.prev_generation = self.create_grid()
        # Current generation
        self.curr_generation = self.create_grid(randomize=randomize)
        # Max generations
        self.max_generations = max_generations
        # Current generation counter
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                if randomize:
                    row.append(random.randint(0, 1))
                else:
                    row.append(0)
            grid.append(row)
        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        row, col = cell
        neighbours = []

        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if i == row and j == col:
                    continue

                if 0 <= i < self.rows and 0 <= j < self.cols:
                    neighbours.append(self.curr_generation[i][j])

        return neighbours

    def get_next_generation(self) -> Grid:
        new_grid = self.create_grid(randomize=False)

        for i in range(self.rows):
            for j in range(self.cols):
                neighbours = self.get_neighbours((i, j))
                alive_neighbours = sum(neighbours)
                current_state = self.curr_generation[i][j]

                if current_state == 1:
                    if alive_neighbours in [2, 3]:
                        new_grid[i][j] = 1
                    else:
                        new_grid[i][j] = 0
                else:
                    if alive_neighbours == 3:
                        new_grid[i][j] = 1
                    else:
                        new_grid[i][j] = 0

        return new_grid

    def step(self) -> None:
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        # 修复点：先检查是否为 None，防止报错
        if self.max_generations is None or self.max_generations == float("inf"):
            return False
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        with open(filename, "r") as f:
            lines = f.readlines()

        grid = []
        for line in lines:
            row = [int(char) for char in line.strip()]
            grid.append(row)

        rows = len(grid)
        cols = len(grid[0]) if rows > 0 else 0

        game = GameOfLife((rows, cols), randomize=False)
        game.curr_generation = grid
        return game

    def save(self, filename: pathlib.Path) -> None:
        with open(filename, "w") as f:
            for row in self.curr_generation:
                line = "".join(str(cell) for cell in row)
                f.write(line + "\n")
