import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        
        # Calculate window width and height based on grid size
        self.width = self.life.cols * cell_size
        self.height = self.life.rows * cell_size
        self.screen_size = self.width, self.height
        self.screen = None

    def draw_lines(self) -> None:
        """ 
        Draws the grid lines. 
        """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        """ 
        Draws the cells. Green for alive, White (background) for dead. 
        """
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                # Calculate the position of the rect
                x = j * self.cell_size
                y = i * self.cell_size
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                
                # If cell is alive (1), draw it green
                if self.life.curr_generation[i][j] == 1:
                    pygame.draw.rect(self.screen, pygame.Color("green"), rect)

    def run(self) -> None:
        """ 
        Main game loop. 
        """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen = pygame.display.set_mode(self.screen_size)
        
        running = True
        paused = False
        
        while running:
            # 1. Handle events (Quit, Pause)
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        paused = not paused
                    
                elif event.type == MOUSEBUTTONDOWN:
                    # Optional: Allow user to toggle cells by clicking
                    click_x, click_y = pygame.mouse.get_pos()
                    grid_x = click_x // self.cell_size
                    grid_y = click_y // self.cell_size
                    # Toggle cell state
                    current = self.life.curr_generation[grid_y][grid_x]
                    self.life.curr_generation[grid_y][grid_x] = 0 if current else 1

            # 2. Draw everything
            self.screen.fill(pygame.Color("white"))
            self.draw_grid()
            self.draw_lines()
            
            # 3. Update game state
            if not paused:
                self.life.step()
            
            # 4. Update display
            pygame.display.flip()
            clock.tick(self.speed)
        
        pygame.quit()
if __name__ == "__main__":
    # 1. 创建游戏逻辑对象 (20行 20列，随机初始化)
    game = GameOfLife((20, 20), randomize=True)
    
    # 2. 创建界面对象
    gui = GUI(game)
    
    # 3. 启动游戏
    gui.run()