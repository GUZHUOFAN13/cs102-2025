import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.screen_size = width, height
        self.screen = pygame.display.set_mode(self.screen_size)
        self.speed = speed
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size
        self.grid = self.create_grid(randomize=True)

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_lines()
            self.draw_grid()
            self.get_next_generation()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = []
        for i in range(self.cell_height):
            row = []
            for j in range(self.cell_width):
                if randomize:
                    row.append(random.randint(0, 1))
                else:
                    row.append(0)
            grid.append(row)
        return grid

    def draw_grid(self) -> None:
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                x = j * self.cell_size
                y = i * self.cell_size
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                if self.grid[i][j] == 1:
                    pygame.draw.rect(self.screen, pygame.Color("green"), rect)

    def get_neighbours(self, cell: Cell) -> Cells:
        row, col = cell
        neighbours = []
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if i == row and j == col:
                    continue
                if 0 <= i < self.cell_height and 0 <= j < self.cell_width:
                    neighbours.append(self.grid[i][j])
        return neighbours

    def get_next_generation(self) -> Grid:
        new_grid = self.create_grid(randomize=False)
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                neighbours = self.get_neighbours((i, j))
                alive_neighbours = sum(neighbours)
                current_state = self.grid[i][j]
                if current_state == 1:
                    if alive_neighbours in [2, 3]:
                        new_grid[i][j] = 1
                else:
                    if alive_neighbours == 3:
                        new_grid[i][j] = 1
        self.grid = new_grid
        return new_grid
