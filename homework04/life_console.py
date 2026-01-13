import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        pass

    def draw_grid(self, screen) -> None:
        pass

    def run(self) -> None:

        pass
