from objparser import Object3D

from constants import RAILS_MAP, Punt

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


def RAILS_OBJ_PATH(type_rails, angle=None):
    num = 3
    name = "recht_" + str(num)

    if type_rails == RAILS_BOCHT:
        num = 6
        name = "bocht_" + str(angle) + "_" + str(num)

    return RAILS_MAP + name + ".obj"


class Rails:
    def __init__(self, pos_x=0, pos_y=0, pos_z=HOOGTE_RAILS, rotation=0,
                 next_rails=None, prev_rails=None, ref_punt_next=None,
                 ref_punt_prev=None):
        self.start_x, self.start_y, self.start_z = (0, 0, 0)
        self.pos = Punt(pos_x, pos_y, pos_z)
        self.rotation = rotation
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
        self.object.render(self.pos, Punt(0, 0, self.rotation),
                           self.is_flipped)

    def move(self, x=None, y=None, z=None):
        x = x + self.start_x if x is not None else self.pos.x
        y = y + self.start_y if y is not None else self.pos.y
        z = z + self.start_z if z is not None else self.pos.z

        if self.ref_punt_prev:
            self.ref_punt_prev = (x - self.pos.x + self.ref_punt_prev[0],
                                  y - self.pos.y + self.ref_punt_prev[1])
        if self.ref_punt_next:
            self.ref_punt_next = (x - self.pos.x + self.ref_punt_next[0],
                                  y - self.pos.y + self.ref_punt_next[1])

        self.pos = Punt(x, y, z)

    def rotate(self, z):
        self.rotation = z

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


class Bocht(Rails):
    def __init__(self, angle, is_flipped=False,
                 pos_x=0, pos_y=0, pos_z=HOOGTE_RAILS,
                 rotation=0, next_rails=None, prev_rails=None,
                 ref_punt_next=None, ref_punt_prev=None, ref_punt_own=None):
        super().__init__(pos_x=pos_x, pos_y=pos_y, pos_z=pos_z,
                         rotation=rotation,
                         next_rails=next_rails, prev_rails=prev_rails,
                         ref_punt_next=ref_punt_next,
                         ref_punt_prev=ref_punt_prev)

        self.angle = angle
        self.is_flipped = is_flipped
        self.image_file = self.image_file(RAILS_BOCHT)
        self.object = self.create_object()
        self.ref_punt_own = ref_punt_own
        self.type = RAILS_BOCHT

    def create_object(self):
        info = RAILS_DEFAULTS_BOCHT_45[self.rotation]
        self.rotation, self.start_x, self.start_y, self.start_z, \
            self.is_flipped, next_prev = info
        self.ref_punt_own = (0, 0)

        if next_prev == NEXT:
            self.ref_punt_next = self.ref_punt_own
        elif next_prev == PREV:
            self.ref_punt_prev = self.ref_punt_own

        self.pos = Punt(self.start_x, self.start_y, self.start_z)

        return Object3D(RAILS_OBJ_PATH(RAILS_BOCHT, self.angle), swap_yz=True)

    def flip(self):
        self.is_flipped = True

    def add_ref_punt(self, ref_punt):
        if self.ref_punt_own == self.ref_punt_next:
            self.ref_punt_prev = ref_punt
        elif self.ref_punt_own == self.ref_punt_prev:
            self.ref_punt_next = ref_punt


class Recht(Rails):
    def __init__(self, is_horizontal=True,
                 pos_x=0, pos_y=0, pos_z=HOOGTE_RAILS,
                 rotation=0, next_rails=None, prev_rails=None,
                 ref_punt_next=None, ref_punt_prev=None):
        super().__init__(pos_x=pos_x, pos_y=pos_y, pos_z=pos_z,
                         rotation=rotation,
                         next_rails=next_rails, prev_rails=prev_rails,
                         ref_punt_next=ref_punt_next,
                         ref_punt_prev=ref_punt_prev)

        self.rotation = 90 * (not is_horizontal | 0)
        self.image_file = self.image_file(RAILS_RECHT)
        self.object = self.create_object()
        self.type = RAILS_RECHT

    def create_object(self):
        # info = RAILS_DEFAULTS_BOCHT_45[self.rotation]
        # self.rotation, self.start_x, self.start_y, self.start_z, \
        #     self.is_flipped = info
        # self.pos = Punt(self.start_x, self.start_y, self.start_z)

        return Object3D(RAILS_OBJ_PATH(RAILS_RECHT), swap_yz=True)
