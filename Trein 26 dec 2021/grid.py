from trein import TREIN_GOEDEREN, TREIN_LOCOMOTIEF, TREIN_PASSAGIER, Trein
from rails import Rails, Bocht, Recht
from ground import create_ground
from poppetje import Poppetje, PoppetjeObject


class Grid:
    def __init__(self):
        self.rails = []
        self.locomotieven = []
        self.goederen = []
        self.passagiers = []
        self.poppetjes = []

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

        for pop in self.poppetjes:
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

        for pop in self.poppetjes:
            pop.render()

    def add_poppetje(self, *args, **kwargs):
        new_pop = Poppetje(*args, **kwargs)
        self.poppetjes.append(new_pop)
        return new_pop

    def add_poppetje2(self, *args, **kwargs):
        """
        name, hat_hair, hat_hair_color, face, trui_color, trui_voor, mouw,
        riem, broek, broek_midden,
        start_x=0, start_y=0, start_z=0, rot_x=0, rot_y=0, rot_z=0,
        figure=None, extra=None
        """
        new_pop = PoppetjeObject(*args, **kwargs)
        self.poppetjes.append(new_pop)
        return new_pop

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

    def add_bocht(self, *args, **kwargs):
        new_rails = Bocht(*args, **kwargs)
        self.rails.append(new_rails)
        return new_rails

    def add_recht(self, *args, **kwargs):
        new_rails = Recht(*args, **kwargs)
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

    def connect_45_bochten(self, rails_prev, rails_next):
        rails_prev.set_next(rails_next)
        rails_next.set_prev(rails_prev)

        rails_prev.add_ref_punt(rails_next.ref_punt_own)
        rails_next.add_ref_punt(rails_prev.ref_punt_own)

    def connect_rails(self, rails_prev, rails_next):
        rails_prev.set_next(rails_next)
        rails_next.set_prev(rails_prev)
