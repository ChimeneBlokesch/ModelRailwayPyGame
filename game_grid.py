from rails import Rails
from train import Train
import pygame

GREEN = (0, 255, 0)

pygame.init()
FONT = pygame.font.Font(None, 15)


class Grid:
    def __init__(self, screen: pygame.Surface, pos, treinen_db):
        self.screen = screen
        self.grid = pygame.Surface(self.screen.get_size())
        self.trains = []
        self.rails = []
        self.treinen_db = treinen_db
        self.pos = pos

    def draw(self):
        self.screen.blit(self.grid, self.pos)
        self.grid.fill(GREEN)
        self.show_coordinate_system()
        [train.draw() for train in self.trains]
        [rails.draw() for rails in self.rails]

    def show_coordinate_system(self):
        step = 50
        for w in range(step, self.grid.get_size()[0], step):
            text_surface = FONT.render(str(w), True, (0, 0, 0))
            self.grid.blit(text_surface, (w, 2))

        for h in range(step, self.grid.get_size()[0], step):
            text_surface = FONT.render(str(h), True, (0, 0, 0))
            self.grid.blit(text_surface, (2, h))

    def add_train(self, start_x, start_y, angle, filename):
        train = Train(self, start_x, start_y, angle, filename)
        self.trains.append(train)

    def add_rails(self, x1, y1, x2, y2):
        rails = Rails(self.grid, x1, y1, x2, y2)
        # rails.draw()
        self.rails.append(rails)
