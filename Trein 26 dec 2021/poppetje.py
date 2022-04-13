import math
import pygame
from objparser import Object3D


from constants import POPPETJES_MAP, SPEEDUP_BOCHT, Punt, TREINEN_MAP, afstand
from position import Position

RUN_SPEED = 0.1
WALK_SPEED = RUN_SPEED / 2
ROTATE_SPEED = 1.5
JUMP_SPEED = 0.1
GRAVITY = -0.01
TERRAIN_HEIGHT = 0

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
        self.rotate_pos = Punt(rot_x, rot_y, rot_z)
        self.pos = Punt(start_x, start_y, start_z)

        self.pos.x, self.pos.y, self.pos.z
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
        # TODO
        temp_pos = Position(*self.pos, *self.rotate_pos)
        self.object.render(temp_pos)

    def move(self, x=None, y=None, z=None):
        x = x if x is not None else self.pos.x
        y = y if y is not None else self.pos.y
        z = z if z is not None else self.pos.z

        self.pos = Punt(x, y, z)
        # print("New pos Pepper", self.pos)

    def rotate(self, x=None, y=None, z=None):
        x = x % 360 if x is not None else self.rotate_pos.x
        y = y % 360 if y is not None else self.rotate_pos.y
        z = z % 360 if z is not None else self.rotate_pos.z

        self.rotate_pos = Punt(x, y, z)

    def move_delta(self, dx=0, dy=0, dz=0):
        self.move(self.pos.x + dx, self.pos.y + dy, self.pos.z + dz)

    def rotate_delta(self, dx=0, dy=0, dz=0):
        self.rotate(self.rotate_pos.x + dx,
                    self.rotate_pos.y + dy,
                    self.rotate_pos.z + dz)

    def walk(self):
        # TODO: als key left/right bij camera.py
        self.rotate_delta(dy=self.turn_speed)

        # if self.turn_speed:
        #     print("turn speed", self.turn_speed)
        #     print("rot_y", self.rotate_pos.y)
        distance = self.speed
        self.up_speed += GRAVITY

        dx = -(distance * math.sin(math.radians(self.rotate_pos.y)))
        dy = (distance * math.cos(math.radians(self.rotate_pos.y)))

        if distance or self.turn_speed:
            print("Pepper", *self.pos, *self.rotate_pos)

        self.move_delta(dx=dx, dy=dy)

        dz = (self.up_speed)
        self.move_delta(dz=dz)

        if self.pos.z < TERRAIN_HEIGHT:
            self.up_speed = 0
            self.move(z=0)
            self.jump_level = 0

    def handle_event(self, event):
        if event.type not in [pygame.KEYDOWN, pygame.KEYUP]:
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
