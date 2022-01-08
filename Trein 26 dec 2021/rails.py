from objparser import Object3D

from constants import RAILS_MAP, Punt

RAILS_RECHT = 0
RAILS_BOCHT = 1
RAILS_WISSEL = 2

RAILS_IMG_FILE = {RAILS_RECHT: "rails_recht.png",
                  RAILS_BOCHT: "rails_bocht.png",
                  RAILS_WISSEL: "rails_wissel.png"}

HOOGTE_RAILS = 0.001

# relatief graden: (absoluut graden, start x, start y, start z = 0.1, flip)
RAILS_DEFAULTS_BOCHT_45 = {0: (180, -2, 0, HOOGTE_RAILS, True),
                           45: (90, 0, 2, HOOGTE_RAILS, False),
                           90: (270, 0, -2, HOOGTE_RAILS, True),
                           135: (180, -2, 0, HOOGTE_RAILS, False),
                           180: (0, 2, 0, HOOGTE_RAILS, True),
                           225: (270, 0, -2, HOOGTE_RAILS, False),
                           270: (90, 0, 2, HOOGTE_RAILS, True),
                           315: (0, 2, 0, HOOGTE_RAILS, False)}


def RAILS_IMG_PATH(type_rails):
    return RAILS_MAP + RAILS_IMG_FILE[type_rails]


def RAILS_OBJ_PATH(type_rails, angle=None):
    num = 3
    name = "recht_" + str(num)

    if type_rails == RAILS_BOCHT:
        num = 6
        name = "bocht_" + str(angle) + "_" + str(num)

    return RAILS_MAP + name + ".obj"


class Rails:
    def __init__(self, type_rails, angle=None, is_flipped=False, pos_x=0,
                 pos_y=0, pos_z=HOOGTE_RAILS, rotation=0, next_rails=None,
                 prev_rails=None, ref_punt_next=None, ref_punt_prev=None):
        self.type = type_rails
        self.angle = angle
        self.start_x, self.start_y, self.start_z = (0, 0, 0)
        self.pos = Punt(pos_x, pos_y, pos_z)
        self.rotation = rotation
        self.is_flipped = is_flipped
        self.image_file = RAILS_IMG_PATH(type_rails)
        self.object = self.create_object()
        self.next = next_rails
        self.prev = prev_rails
        self.ref_punt_next = ref_punt_next
        self.ref_punt_prev = ref_punt_prev

    def create_object(self):
        if self.type == RAILS_BOCHT and self.angle == 45:
            info = RAILS_DEFAULTS_BOCHT_45[self.rotation]
            self.rotation, self.start_x, self.start_y, self.start_z, \
                self.is_flipped = info
            self.pos = Punt(self.start_x, self.start_y, self.start_z)

        return Object3D(RAILS_OBJ_PATH(self.type, self.angle), swap_yz=True)

    def generate(self):
        return self.object.generate()

    def render(self):
        self.object.render(self.pos, Punt(0, 0, self.rotation),
                           self.is_flipped)

    def move(self, x=None, y=None, z=None):
        x = x + self.start_x if x is not None else self.pos.x
        y = y + self.start_y if y is not None else self.pos.y
        z = z + self.start_z if z is not None else self.pos.z

        self.pos = Punt(x, y, z)

    def rotate(self, z):
        self.rotation = z

    def flip(self):
        self.is_flipped = True

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


# Misschien
# class Bocht(Rails)
