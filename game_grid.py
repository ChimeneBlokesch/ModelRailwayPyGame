from train import Train
import pygame

GREEN = (0, 255, 0)


class Grid:
    def __init__(self, screen: pygame.Surface, pos, treinen_db):
        self.screen = screen
        self.grid = pygame.Surface(self.screen.get_size())
        self.trains = []
        self.treinen_db = treinen_db
        self.pos = pos

    def draw(self):
        self.screen.blit(self.grid, self.pos)
        self.grid.fill(GREEN)
        [train.draw() for train in self.trains]

    def add_train(self, start_x, start_y, angle, filename):
        train = Train(self, start_x, start_y, angle, filename)
        self.trains.append(train)
