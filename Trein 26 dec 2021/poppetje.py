import math
from objparser import Object3D

from constants import POPPETJES_MAP, SPEEDUP_BOCHT, Punt, TREINEN_MAP, afstand, getFrameTimeSeconds

RUN_SPEED = 0.1
WALK_SPEED = 0.05


class Poppetje:
    def __init__(self, name, obj_name, start_x=0, start_y=0, start_z=0,
                 rot_x=0, rot_y=0, rot_z=0):
        self.name = name
        self.obj_name = obj_name
        self.object = self.create_object()
        self.start_angle = 0
        self.speed = 0
        self.turn_speed = 0
        self.rotate_pos = Punt(rot_x, rot_y, rot_z)
        self.pos = Punt(start_x, start_y, start_z)
        self.is_player = False

    def create_object(self):
        # TODO: change to general poppetje and always change_img
        model = Object3D(POPPETJES_MAP, self.obj_name)

        # if self.mtl_images:
        #     model.change_img(self.mtl_images)

        return model

    def generate(self):
        self.object.generate()

    def render(self):
        self.object.render(self.pos, self.rotate_pos, scale_value=(2, 2, 2))

    def move(self, x=None, y=None, z=None):
        x = x if x is not None else self.pos.x
        y = y if y is not None else self.pos.y
        z = z if z is not None else self.pos.z

        self.pos = Punt(x, y, z)

    def rotate(self, x=None, y=None, z=None):
        x = x if x is not None else self.rotate_pos.x
        y = y if y is not None else self.rotate_pos.y
        z = z if z is not None else self.rotate_pos.z

        self.rotate_pos = Punt(x, y, z)

    def walk(self):
        rot_y = self.turn_speed * getFrameTimeSeconds()
