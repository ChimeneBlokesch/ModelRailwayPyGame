import pygame

from rails import Rails, RailsType
from train import Train

GREEN = (0, 255, 0)

pygame.init()
FONT = pygame.font.Font(None, 15)


class Grid:
    def __init__(self, screen: pygame.Surface, pos, trains_db):
        self.screen = screen
        self.screen_grid = pygame.Surface(self.screen.get_size())
        self.trains: list[Train] = []
        self.rails = []
        self.trains_db = trains_db
        self.pos = pos
        self.wissels = []

    def draw(self):
        self.screen.blit(self.screen_grid, self.pos)
        self.screen_grid.fill(GREEN)
        self.show_coordinate_system()
        [rails.draw(self.screen_grid) for rails in self.rails]
        [train.draw(self.screen_grid) for train in self.trains]

    def show_coordinate_system(self):
        step = 50
        for w in range(step, self.screen_grid.get_size()[0], step):
            text_surface = FONT.render(str(w), True, (0, 0, 0))
            self.screen_grid.blit(text_surface, (w, 2))

        for h in range(step, self.screen_grid.get_size()[0], step):
            text_surface = FONT.render(str(h), True, (0, 0, 0))
            self.screen_grid.blit(text_surface, (2, h))

    def add_train(self, start_x, start_y, angle, filename):
        train = Train(self.trains_db, start_x, start_y, angle, filename)
        self.trains.append(train)

    def add_rails(self, type_rails: RailsType, x1, y1, x2, y2):
        rails = Rails(type_rails, x1, y1, x2, y2)
        self.rails.append(rails)
