from typing import List

from train import TRAIN_GOEDEREN, TRAIN_LOCOMOTIEF, TRAIN_PASSAGIER, Train
from rails import Rails, Curve, Straight
from ground import create_ground
from character_model import CharacterModel


class Grid:
    def __init__(self):
        self.rails: List[Rails] = []
        self.engines: List[Train] = []
        self.goederen: List[Train] = []
        self.passagiers: List[Train] = []
        self.characters: list[CharacterModel] = []

    def generate(self):
        for rails in self.rails:
            rails.generate()

        for train in self.engines:
            train.generate()
        for train in self.passagiers:
            train.generate()
        for train in self.goederen:
            train.generate()

        for pop in self.characters:
            pop.generate()

    def render(self):
        # create_assenstelsel()
        # create_grid()
        create_ground()

        for rails in self.rails:
            rails.render()

        for train in self.engines:
            train.render()

        for train in self.passagiers:
            train.render()

        for train in self.goederen:
            train.render()

        for pop in self.characters:
            pop.render()

    def add_character(self, character: CharacterModel):
        self.characters.append(character)

    def add_train(self, train: Train):
        type2arr = {TRAIN_LOCOMOTIEF: self.engines,
                    TRAIN_PASSAGIER: self.passagiers,
                    TRAIN_GOEDEREN: self.goederen}
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

    def rijden(self):
        for train in self.engines:
            train.rijden()

        for train in self.passagiers:
            train.rijden()

        for train in self.goederen:
            train.rijden()

        self.render()

    def connect_45_curves(self, rails_prev, rails_next):
        rails_prev.set_next(rails_next)
        rails_next.set_prev(rails_prev)

        rails_prev.add_ref_punt(rails_next.ref_punt_own)
        rails_next.add_ref_punt(rails_prev.ref_punt_own)

    def connect_rails(self, rails_prev, rails_next):
        rails_prev.set_next(rails_next)
        rails_next.set_prev(rails_prev)
