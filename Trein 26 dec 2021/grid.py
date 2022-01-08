from trein import Trein
from rails import HOOGTE_RAILS, Rails, Bocht, Recht
from ground import create_assenstelsel, create_grid, create_ground


class Grid:
    def __init__(self):
        self.rails = []
        self.treinen = []

    def generate(self):
        for rails in self.rails:
            rails.generate()

        for trein in self.treinen:
            trein.generate()

    def render(self):
        create_assenstelsel()
        create_grid()
        create_ground()

        for rails in self.rails:
            rails.render()

        for trein in self.treinen:
            trein.render()

    def add_trein(self, name, filename, x, y):
        new_trein = Trein(name, filename, x, y)
        self.treinen.append(new_trein)
        return new_trein

    def add_rails(self, type_rails, angle=None, is_flipped=False, pos_x=0,
                  pos_y=0, pos_z=HOOGTE_RAILS, rotation=0, next_rails=None,
                  prev_rails=None, ref_punt_next=None, ref_punt_prev=None):
        new_rails = Rails(type_rails, angle, is_flipped, pos_x,
                          pos_y, pos_z, rotation, next_rails,
                          prev_rails, ref_punt_next, ref_punt_prev)
        self.rails.append(new_rails)
        return new_rails

    def add_bocht(self, angle, is_flipped=False,
                  pos_x=0, pos_y=0, pos_z=HOOGTE_RAILS,
                  rotation=0, next_rails=None, prev_rails=None,
                  ref_punt_next=None, ref_punt_prev=None):
        new_rails = Bocht(angle, is_flipped=is_flipped, pos_x=pos_x,
                          pos_y=pos_y, pos_z=pos_z, rotation=rotation,
                          next_rails=next_rails, prev_rails=prev_rails,
                          ref_punt_next=ref_punt_next,
                          ref_punt_prev=ref_punt_prev)
        self.rails.append(new_rails)
        return new_rails

    def add_recht(self, is_horizontal=True,
                  pos_x=0, pos_y=0, pos_z=HOOGTE_RAILS,
                  rotation=0, next_rails=None, prev_rails=None,
                  ref_punt_next=None, ref_punt_prev=None):
        new_rails = Recht(is_horizontal,
                          pos_x=pos_x, pos_y=pos_y, pos_z=pos_z,
                          rotation=rotation,
                          next_rails=next_rails, prev_rails=prev_rails,
                          ref_punt_next=ref_punt_next,
                          ref_punt_prev=ref_punt_prev)
        self.rails.append(new_rails)
        return new_rails

    def rijden(self):
        for trein in self.treinen:
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
