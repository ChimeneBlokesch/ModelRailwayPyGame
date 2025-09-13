from typing import List

from train import TRAIN_FREIGHT, TRAIN_ENGINE, TRAIN_PASSENGER, Train
from rails import Rails, Curve, Straight
from ground import create_ground
from character_model import CharacterModel


class Grid:
    def __init__(self):
        self.rails: List[Rails] = []
        self.engines: List[Train] = []
        self.freight_cars: List[Train] = []
        self.passenger_cars: List[Train] = []
        self.characters: list[CharacterModel] = []

    def generate(self):
        for rails in self.rails:
            rails.generate()

        for train in self.engines:
            train.generate()
        for train in self.passenger_cars:
            train.generate()
        for train in self.freight_cars:
            train.generate()

        for character in self.characters:
            character.generate()

    def render(self):
        # create_grid_lines()
        # create_grid()
        create_ground()

        for rails in self.rails:
            rails.render()

        for train in self.engines:
            train.render()

        for train in self.passenger_cars:
            train.render()

        for train in self.freight_cars:
            train.render()

        for character in self.characters:
            character.render()

    def add_character(self, character: CharacterModel):
        self.characters.append(character)

    def add_train(self, train: Train):
        type2arr = {TRAIN_ENGINE: self.engines,
                    TRAIN_PASSENGER: self.passenger_cars,
                    TRAIN_FREIGHT: self.freight_cars}
        arr = type2arr[train.type]
        arr.append(train)

    def add_rails(self, *args, **kwargs):
        new_rails = Rails(*args, **kwargs)
        self.rails.append(new_rails)
        return new_rails

    def add_curve(self, *args, **kwargs):
        new_rails = Curve(*args, **kwargs)
        self.rails.append(new_rails)
        return new_rails

    def add_straight(self, *args, **kwargs):
        new_rails = Straight(*args, **kwargs)
        self.rails.append(new_rails)
        return new_rails

    def drive(self):
        for train in self.engines:
            train.drive()

        for train in self.passenger_cars:
            train.drive()

        for train in self.freight_cars:
            train.drive()

        self.render()

    def connect_45_curves(self, rails_prev: Straight | Curve,
                          rails_next: Straight | Curve):
        rails_prev.set_next(rails_next)
        rails_next.set_prev(rails_prev)

        rails_prev.add_ref_punt(rails_next.ref_punt_own)
        rails_next.add_ref_punt(rails_prev.ref_punt_own)

    def connect_rails(self, rails_prev: Straight | Curve,
                      rails_next: Straight | Curve):
        rails_prev.set_next(rails_next)
        rails_next.set_prev(rails_prev)
