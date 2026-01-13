import typing as tp

import pygame

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        pass

    def draw_lines(self) -> None:
        pass

    def run(self) -> None:
        pass

    def create_grid(self, randomize: bool = False) -> Grid:
        return []

    def draw_grid(self) -> None:
        pass

    def get_neighbours(self, cell: Cell) -> Cells:
        return []

    def get_next_generation(self) -> Grid:
        return []
