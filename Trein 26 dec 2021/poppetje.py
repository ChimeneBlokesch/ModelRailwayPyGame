import math
import pygame
from basis_object import BasisObject
from objparser import Object3D


from constants import POPPETJES_MAP, SPEEDUP_BOCHT, TREINEN_MAP, afstand
from position import Position

RUN_SPEED = 0.1
WALK_SPEED = RUN_SPEED / 2
ROTATE_SPEED = 1.5
JUMP_SPEED = 0.1
GRAVITY = -0.01
TERRAIN_HEIGHT = 0

# TODO: put in constants.py
POPPETJES2_MAP = "Poppetjes2/"

pygame.init()


class Poppetje:
    def __init__(self, name, obj_name, start_x=0, start_y=0, start_z=0,
                 rot_x=0, rot_y=0, rot_z=0):
        self.name = name
        self.obj_name = obj_name
        self.object = self.create_object()
        self.start_angle = 0
        self.speed = 0
        self.turn_speed = 0
        self.up_speed = 0

        self.pos = Position(start_x, start_y, start_z, rot_x, rot_y, rot_z)
        self.is_player = False
        self.jump_level = 0  # 0: on ground, 1: small jump, 2: big jump

    def create_object(self):
        # TODO: change to general poppetje and always change_img
        model = Object3D(POPPETJES_MAP, self.obj_name)

        # if self.mtl_images:
        #     model.change_img(self.mtl_images)

        return model

    def generate(self):
        self.object.generate()

    def render(self):
        self.object.render(self.pos)

    def walk(self):
        # TODO: als key left/right bij camera.py
        self.pos.rotate_delta(dy=self.turn_speed)

        # if self.turn_speed:
        #     print("turn speed", self.turn_speed)
        #     print("rot_y", self.rotate_pos.y)
        distance = self.speed
        self.up_speed += GRAVITY

        dx = -(distance * math.sin(math.radians(self.pos.ry)))
        dy = (distance * math.cos(math.radians(self.pos.ry)))

        if distance or self.turn_speed:
            print("Pepper", *
                  (self.pos.get_pos()), *(self.pos.get_rotate()))

        self.pos.move_delta(dx=dx, dy=dy)

        dz = (self.up_speed)
        self.pos.move_delta(dz=dz)

        if self.pos.z < TERRAIN_HEIGHT:
            self.up_speed = 0
            self.pos.move(z=0)
            self.jump_level = 0

    def handle_event(self, event):
        if event.type not in [pygame.KEYDOWN, pygame.KEYUP]:
            return

        if pygame.key.get_pressed()[pygame.K_LCTRL]:
            return

        if event.key == pygame.K_UP:
            self.speed = -RUN_SPEED if event.type == pygame.KEYDOWN else 0
        elif event.key == pygame.K_DOWN:
            self.speed = RUN_SPEED if event.type == pygame.KEYDOWN else 0
        elif event.key == pygame.K_LEFT:
            self.turn_speed = ROTATE_SPEED \
                if event.type == pygame.KEYDOWN else 0
            # self.speed = -RUN_SPEED if event.type == pygame.KEYDOWN else 0
        elif event.key == pygame.K_RIGHT:
            self.turn_speed = -ROTATE_SPEED \
                if event.type == pygame.KEYDOWN else 0
            # self.speed = -RUN_SPEED if event.type == pygame.KEYDOWN else 0
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RSHIFT:
            self.jump()

    def jump(self):
        if self.jump_level < 2:
            self.up_speed = JUMP_SPEED
            self.jump_level += 1


class PoppetjeObject:
    """
    Keeps track of all models of a figure.
    Eventually also able to move and rotate part of the models with this class.
    """

    # , trui, mouw, riem, broek, broek_midden, extra=[]
    def __init__(self, name, hat_hair, hat_hair_color, face, trui_color, trui_voor, start_x=0, start_y=0, start_z=0,
                 rot_x=0, rot_y=0, rot_z=0):
        self.name = name
        self.pos = Position(start_x, start_y, start_z, rot_x, rot_y, rot_z)
        self.hat = HatHair(hat_hair, hat_hair_color, start_x,
                           start_y, start_z, rot_x, rot_y, rot_z)
        self.head = Head("head", face, start_x, start_y,
                         start_z, rot_x, rot_y, rot_z)
        self.trui = Trui("trui", trui_color, trui_voor, start_x,
                         start_y, start_z, rot_x, rot_y, rot_z)

    def generate(self):
        for o in [self.hat, self.head, self.trui]:
            o.generate()

    def render(self):
        for o in [self.hat, self.head, self.trui]:
            o.render()


class HatHair(BasisObject):
    def __init__(self, obj, color, start_x=0, start_y=0, start_z=0, rot_x=0, rot_y=0, rot_z=0):
        # Color (r, g, b)
        mtl_images = {"hathair": (False, color)}
        super().__init__(obj, POPPETJES2_MAP, start_x, start_y,
                         start_z, rot_x, rot_y, rot_z, mtl_images)

    def change_color(self, color):
        mtl_images = {"hathair": (False, color)}
        self.object.change_img(mtl_images, POPPETJES2_MAP)


class Head(BasisObject):
    def __init__(self, obj, face_name, start_x=0, start_y=0, start_z=0, rot_x=0, rot_y=0, rot_z=0):
        self.face_name = face_name
        mtl_images = {"face": (True, face_name + "_face" + "0")}
        super().__init__(obj, POPPETJES2_MAP, start_x, start_y,
                         start_z, rot_x, rot_y, rot_z, mtl_images)

    def change_emotion(self, num):
        mtl_images = {"face": (True, self.face_name + str(num))}
        self.object.change_img(mtl_images, POPPETJES2_MAP)

    def change_face(self, face_name, num=0):
        self.face_name = face_name
        mtl_images = {"face": (True, self.face_name + str(num))}
        self.object.change_img(mtl_images, POPPETJES2_MAP)


class Trui(BasisObject):
    def __init__(self, obj, trui_color, trui_voor, start_x=0, start_y=0, start_z=0, rot_x=0, rot_y=0, rot_z=0):
        self.trui_color = trui_color
        mtl_images = {"trui": (False, trui_color),
                      "trui_voor": (True, trui_voor + "_trui_voor")}
        super().__init__(obj, POPPETJES2_MAP, start_x, start_y,
                         start_z, rot_x, rot_y, rot_z, mtl_images)

    def change_trui_voor(self, trui_voor):
        mtl_images = {"trui": (True, trui_voor + "_trui_voor")}
        self.object.change_img(mtl_images, POPPETJES2_MAP)

    def change_trui_color(self, color):
        mtl_images = {"trui": (False, color)}
        self.object.change_img(mtl_images, POPPETJES2_MAP)
