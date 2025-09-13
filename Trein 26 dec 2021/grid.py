from train import TREIN_GOEDEREN, TREIN_LOCOMOTIEF, TREIN_PASSAGIER, Trein
from rails import Rails, Curve, Straight
from ground import create_ground
from character_model import CharacterModel


class Grid:
    def __init__(self):
        self.rails = []
        self.locomotieven = []
        self.goederen = []
        self.passagiers = []
        self.characters: list[CharacterModel] = []

    def generate(self):
        for rails in self.rails:
            rails.generate()

        # for trein in self.treinen:
        for trein in self.locomotieven:
            trein.generate()
        for trein in self.passagiers:
            trein.generate()
        for trein in self.goederen:
            trein.generate()

        for pop in self.characters:
            pop.generate()

    def render(self):
        # create_assenstelsel()
        # create_grid()
        create_ground()

        for rails in self.rails:
            rails.render()

        # for trein in self.treinen:
        for trein in self.locomotieven:
            trein.render()

        for trein in self.passagiers:
            trein.render()

        for trein in self.goederen:
            trein.render()

        for pop in self.characters:
            pop.render()

    def add_character(self, character: CharacterModel):
        self.characters.append(character)

    def add_train(self, train: Trein):
        type2arr = {TREIN_LOCOMOTIEF: self.locomotieven,
                    TREIN_PASSAGIER: self.passagiers,
                    TREIN_GOEDEREN: self.goederen}
        arr = type2arr[train.type]
        arr.append(train)

    def add_trein(self, *args, **kwargs):
        new_trein = Trein(*args, **kwargs)

        type_trein = new_trein.type
        if type_trein == TREIN_LOCOMOTIEF:
            self.locomotieven.append(new_trein)
        elif type_trein == TREIN_PASSAGIER:
            self.passagiers.append(new_trein)
        elif type_trein == TREIN_GOEDEREN:
            self.goederen.append(new_trein)

        return new_trein

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
        for trein in self.locomotieven:
            trein.rijden()

        for trein in self.passagiers:
            trein.rijden()

        for trein in self.goederen:
            trein.rijden()

        self.render()

    def connect_45_curves(self, rails_prev, rails_next):
        rails_prev.set_next(rails_next)
        rails_next.set_prev(rails_prev)

        rails_prev.add_ref_punt(rails_next.ref_punt_own)
        rails_next.add_ref_punt(rails_prev.ref_punt_own)

    def connect_rails(self, rails_prev, rails_next):
        rails_prev.set_next(rails_next)
        rails_next.set_prev(rails_prev)
