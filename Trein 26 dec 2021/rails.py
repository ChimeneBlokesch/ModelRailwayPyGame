from objparser import Object3D

from constants import RAILS_MAP
from position import Position
import numpy as np

RAILS_RECHT = 0
RAILS_BOCHT = 1
RAILS_WISSEL = 2

RAILS_IMG_FILE = {RAILS_RECHT: "rails_recht.png",
                  RAILS_BOCHT: "rails_bocht.png",
                  RAILS_WISSEL: "rails_wissel.png"}

HOOGTE_RAILS = 0.001

NEXT = 0
PREV = 1

# relatief graden: (absoluut graden, start x, start y, flip,next/prev ref_punt)
RAILS_DEFAULTS_BOCHT_45 = {0: (180, -2, 0, HOOGTE_RAILS, True, NEXT),
                           45: (90, 0, 2, HOOGTE_RAILS, False, PREV),
                           90: (270, 0, -2, HOOGTE_RAILS, True, NEXT),
                           135: (180, -2, 0, HOOGTE_RAILS, False, PREV),
                           180: (0, 2, 0, HOOGTE_RAILS, True, NEXT),
                           225: (270, 0, -2, HOOGTE_RAILS, False, PREV),
                           270: (90, 0, 2, HOOGTE_RAILS, True, NEXT),
                           315: (0, 2, 0, HOOGTE_RAILS, False, PREV)}


def RAILS_IMG_PATH(type_rails):
    return RAILS_MAP + RAILS_IMG_FILE[type_rails]


def RAILS_OBJ_NAME(type_rails, angle=None):
    num = 3
    name = "recht_" + str(num)

    if type_rails == RAILS_BOCHT:
        num = 6
        name = "bocht_" + str(angle) + "_" + str(num)

    return name


def REF_PUNT_RECHT(is_horizontal, go_left_down):
    if is_horizontal and go_left_down:
        return (2, 0), (-2, 0)

    if is_horizontal:
        return (-2, 0), (2, 0)

    if go_left_down:
        return (0, 2), (0, -2)

    return (0, -2), (0, 2)


class Rails:
    def __init__(self, name, pos_x=0, pos_y=0, pos_z=HOOGTE_RAILS, rotation=0,
                 next_rails=None, prev_rails=None, ref_punt_next=None,
                 ref_punt_prev=None):
        self.name = name
        self.start_x, self.start_y, self.start_z = (0, 0, 0)

        # Only uses z-axis to rotate.
        self.pos = Position(x=pos_x, y=pos_y, z=pos_z, rz=rotation)

        self.image_file = lambda type_rails: RAILS_IMG_PATH(type_rails)
        self.next = next_rails
        self.prev = prev_rails
        self.ref_punt_next = ref_punt_next
        self.ref_punt_prev = ref_punt_prev
        self.object = None
        self.is_flipped = False

    def generate(self):
        return self.object.generate()

    def render(self):
        self.object.render(self.pos, self.is_flipped,
                           scale_value=(2, 2, 0))

    def move(self, x=None, y=None, z=None, add_start=True):
        x = x + self.start_x * add_start if x is not None else self.pos.x
        y = y + self.start_y * add_start if y is not None else self.pos.y
        z = z + self.start_z * add_start if z is not None else self.pos.z

        if self.ref_punt_prev:
            self.ref_punt_prev = (x - self.pos.x + self.ref_punt_prev[0],
                                  y - self.pos.y + self.ref_punt_prev[1])
        if self.ref_punt_next:
            self.ref_punt_next = (x - self.pos.x + self.ref_punt_next[0],
                                  y - self.pos.y + self.ref_punt_next[1])

        self.pos.move(x, y, z)

    def rotate(self, z):
        self.pos.rotate(z=z)

    def get_ref_punt(self):
        if self.ref_punt_next:
            return self.ref_punt_next

        return self.ref_punt_prev

    def get_ref_punten(self):
        return self.ref_punt_prev, self.ref_punt_next

    def set_next(self, rails):
        self.next = rails

    def set_prev(self, rails):
        self.prev = rails

    def get_rotation(self):
        return self.pos.rz


class Bocht(Rails):
    def __init__(self, name, angle, is_flipped=False,
                 pos_x=0, pos_y=0, pos_z=HOOGTE_RAILS,
                 rotation=0, next_rails=None, prev_rails=None,
                 ref_punt_next=None, ref_punt_prev=None, ref_punt_own=None,
                 own_next_prev=NEXT):
        super().__init__(name, pos_x=pos_x, pos_y=pos_y, pos_z=pos_z,
                         rotation=rotation,
                         next_rails=next_rails, prev_rails=prev_rails,
                         ref_punt_next=ref_punt_next,
                         ref_punt_prev=ref_punt_prev)

        self.angle = angle
        self.is_flipped = is_flipped
        self.own_next_prev = own_next_prev
        self.ref_punt_own = ref_punt_own
        self.image_file = self.image_file(RAILS_BOCHT)
        self.relative_rotation = rotation
        self.object = self.create_object()

        self.type = RAILS_BOCHT

    def create_object(self):
        info = RAILS_DEFAULTS_BOCHT_45[self.relative_rotation]
        rotation, self.start_x, self.start_y, self.start_z, \
            self.is_flipped, next_prev = info
        self.ref_punt_own = (0, 0)

        self.pos.rotate(z=rotation)

        if next_prev == NEXT:
            self.ref_punt_next = self.ref_punt_own
        elif next_prev == PREV:
            self.ref_punt_prev = self.ref_punt_own

        self.own_next_prev = next_prev
        self.pos.move(self.start_x, self.start_y, self.start_z)

        return Object3D(RAILS_MAP, RAILS_OBJ_NAME(RAILS_BOCHT, self.angle), swap_yz=True)

    def flip(self):
        self.is_flipped = True

    def add_ref_punt(self, ref_punt):
        if self.own_next_prev == NEXT:
            self.ref_punt_prev = ref_punt
        elif self.own_next_prev == PREV:
            self.ref_punt_next = ref_punt

    def move(self, x, y, z=None, add_start=True):
        z = z if z is not None else self.pos.z
        super().move(x=x, y=y, z=z, add_start=add_start)

        if self.own_next_prev == NEXT:
            self.ref_punt_own = self.ref_punt_next
        elif self.own_next_prev == PREV:
            self.ref_punt_own = self.ref_punt_prev


class Recht(Rails):
    def __init__(self, name, is_horizontal=True, go_left_down=False,
                 pos_x=0, pos_y=0, pos_z=HOOGTE_RAILS,
                 rotation=0, next_rails=None, prev_rails=None):
        ref_punt_prev, ref_punt_next = REF_PUNT_RECHT(
            is_horizontal, go_left_down)
        super().__init__(name, pos_x=pos_x, pos_y=pos_y, pos_z=pos_z,
                         rotation=rotation,
                         next_rails=next_rails, prev_rails=prev_rails,
                         ref_punt_next=ref_punt_next,
                         ref_punt_prev=ref_punt_prev)

        self.pos.rotate(z=90 * (not is_horizontal | 0))
        self.image_file = self.image_file(RAILS_RECHT)
        self.object = self.create_object()
        self.type = RAILS_RECHT
        self.go_left_down = go_left_down

    def create_object(self):
        return Object3D(RAILS_MAP, RAILS_OBJ_NAME(RAILS_RECHT), swap_yz=True)
