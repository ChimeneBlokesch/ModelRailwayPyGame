from __future__ import annotations
import pygame

from database_trains import TrainFormat

WIDTH = 100

LENGTH = 20


class Train:
    def __init__(self, properties: TrainFormat, start_x: int, start_y: int,
                 angle: int, folder: str):
        self.x = start_x
        self.y = start_y
        self.angle = angle
        self.speed = 0
        self.max_speed = 10
        self.folder = folder
        self.properties = properties

        self.train_before = None
        self.train_after = None

    def draw(self, screen: pygame.Surface):
        try:
            filepath = self.properties.get_sprite_file_path(self.angle)
            train = pygame.image.load(filepath)
        except FileNotFoundError:
            return

        size = train.get_size()
        height = size[1] * WIDTH / size[0]
        train = pygame.transform.smoothscale(train, (WIDTH, height))
        # train = pygame.transform.rotate(train, self.angle)
        screen.blit(train, (self.x, self.y - 0.5 * height))

    def attach_front(self, train: Train):
        self.train_before = train

    def detach_front(self):
        self.train_before = None

    def attach_back(self, train: Train):
        self.train_after = train

    def detach_back(self):
        self.train_after = None
