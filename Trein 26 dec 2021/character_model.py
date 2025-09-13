from __future__ import annotations
import math
import numpy as np
import pygame
from basis_object import BasisObject


from constants import CHARACTER_FOLDER, e2h, h2e
from position import Position


RUN_SPEED = 0.1
WALK_SPEED = RUN_SPEED / 2
ROTATE_SPEED = 1.5
JUMP_SPEED = 0.1
GRAVITY = -0.01
TERRAIN_HEIGHT = 0

RUN_SPEED2 = 10
WALK_SPEED2 = RUN_SPEED2 / 2


pygame.init()


class CharacterModel:
    """
    Keeps track of all models of a figure.
    Also able to move and rotate part of the models with this class.
    """

    def __init__(self, name,
                 hair: Hair,
                 head: Head,
                 shirt: Shirt,
                 arms: Arms,
                 legs: Legs,
                 start_x=0, start_y=0, start_z=0,
                 rot_x=0, rot_y=0, rot_z=0):
        """
        Colors should be given as the tuple (r, g, b) and not gamma corrected.
        """
        self.name = name
        self.direction = 100
        self.speed = 0
        self.start_angle = 0
        self.turn_speed = 0
        self.up_speed = 0

        self.is_player = False
        self.jump_level = 0  # 0: on ground, 1: small jump, 2: big jump
        self.pos = Position(start_x, start_y, start_z,
                            rot_x, rot_y, rot_z)

        self.legs = legs

        self.objects = [hair, head, shirt, arms, legs]

    def generate(self):
        for o in self.objects:
            o.generate()

    def render(self):
        self.move_legs()

        for o in self.objects:
            o.render()

    def move_legs(self):
        if self.speed == 0:
            self.legs.l_leg.extra_rot = 0
            self.legs.r_leg.extra_rot = 0
            return

        if self.legs.l_leg.extra_rot > 50 or self.legs.r_leg.extra_rot > 50:
            self.direction *= -1

        self.legs.l_leg.extra_rot += self.direction * self.speed
        self.legs.r_leg.extra_rot += -self.direction * self.speed

    def move_delta(self, dx=0, dy=0, dz=0):
        self.pos.move_delta(dx, dy, dz)

        for o in self.objects:
            o.move_delta(dx, dy, dz)

    def rotate_delta(self, dx=0, dy=0, dz=0):
        self.pos.rotate_delta(dx, dy, dz)

        for o in self.objects:
            o.rotate_delta(dx, dy, dz)

    def walk(self):
        self.rotate_delta(dy=self.turn_speed)

        distance = self.speed
        self.up_speed += GRAVITY

        dx = -(distance * math.sin(math.radians(self.pos.ry)))
        dy = (distance * math.cos(math.radians(self.pos.ry)))

        self.move_delta(dx=dx, dy=dy)

        if self.pos.z >= TERRAIN_HEIGHT:
            # Above terrain, apply gravity
            dz = (self.up_speed)
            self.move_delta(dz=dz)
            return

        # Keep character at ground
        self.up_speed = 0
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
        if self.jump_level >= 2:
            return

        self.up_speed = JUMP_SPEED
        self.jump_level += 1


class Hair(BasisObject):
    def __init__(self, mid: Position, hair_color, start_x=0, start_y=0, start_z=0,
                 rot_x=0, rot_y=0, rot_z=0):
        self.mid = mid

        # Color (r, g, b)
        mtl_images = {"hair": hair_color}

        super().__init__("hair", CHARACTER_FOLDER,
                         mid.x + start_x,
                         mid.y + start_y,
                         mid.z + start_z,
                         mid.rx + rot_x,
                         mid.ry + rot_y,
                         mid.rz + rot_z,
                         mtl_images)

    def change_color(self, color):
        mtl_images = {"hair": color}
        self.object.change_img(mtl_images, CHARACTER_FOLDER)

    def rotate_delta(self, dx=0, dy=0, dz=0):
        super().rotate_delta(dx, dy, dz)

        if not dy:
            return

        return

        # Translation matrix
        T = np.array([[1, 0, self.mid.x], [0, 1, self.mid.y], [0, 0, 1]])

        # Rotation matrix
        phi = np.radians(dy)
        cp = np.cos(-phi)
        sp = np.sin(-phi)
        R_inv = np.array([[cp, sp, 0], [-sp, cp, 0], [0, 0, 1]])

        # Transformation matrix
        A = T @ R_inv @  np.linalg.inv(T)

        # Rotate around mid to move the hair
        new_x, new_y = h2e(
            A @ e2h(np.array([self.pos.x, self.pos.y])))
        self.pos.move(x=new_x, y=new_y)


class Head(BasisObject):
    def __init__(self, mid: Position, skin_color,
                 start_x=0, start_y=0, start_z=0,
                 rot_x=0, rot_y=0, rot_z=0):
        self.mid = mid
        mtl_images = {"skin": skin_color}

        obj = "head"
        super().__init__(obj, CHARACTER_FOLDER,
                         mid.x + start_x,
                         mid.y + start_y,
                         mid.z + start_z,
                         mid.rx + rot_x,
                         mid.ry + rot_y,
                         mid.rz + rot_z,
                         mtl_images)


class Shirt(BasisObject):
    def __init__(self, mid: Position, shirt_color, pants_color,
                 start_x=0, start_y=0, start_z=0,
                 rot_x=0, rot_y=0, rot_z=0):
        self.mid = mid
        self.shirt_color = shirt_color
        mtl_images = {"shirt": shirt_color,
                      "pants": pants_color}

        super().__init__("shirt", CHARACTER_FOLDER,
                         mid.x + start_x,
                         mid.y + start_y,
                         mid.z + start_z,
                         mid.rx + rot_x,
                         mid.ry + rot_y,
                         mid.rz + rot_z,
                         mtl_images)

    def change_shirt_color(self, color):
        mtl_images = {"shirt": color}
        self.object.change_img(mtl_images, CHARACTER_FOLDER)


class Arms:
    def __init__(self, mid: Position, skin_color, sleeve_color,
                 start_x=0, start_y=0, start_z=0,
                 rot_x=0, rot_y=0, rot_z=0):
        self.mid = mid

        self.l_arm = Arm(mid, skin_color, sleeve_color,
                         start_x, start_y, start_z,
                         rot_x, rot_y, rot_z,
                         is_left=True)

        self.r_arm = Arm(mid, skin_color, sleeve_color,
                         start_x, start_y, start_z,
                         rot_x, rot_y, rot_z,
                         is_left=False)

    def generate(self):
        for o in [self.l_arm, self.r_arm]:
            o.generate()

    def render(self):
        for o in [self.l_arm, self.r_arm]:
            o.render()

    def move_delta(self, dx=0, dy=0, dz=0):
        self.l_arm.move_delta(dx, dy, dz)
        self.r_arm.move_delta(dx, dy, dz)

    def rotate_delta(self, dx=0, dy=0, dz=0):
        self.l_arm.rotate_delta(dx, dy, dz)
        self.r_arm.rotate_delta(dx, dy, dz)

        if not dy:
            return

        return

        # Translation matrix
        T = np.array(
            [[1, 0, self.mid.x], [0, 1, self.mid.y], [0, 0, 1]])

        # Rotation matrix
        phi = np.radians(dy)
        cp = np.cos(-phi)
        sp = np.sin(-phi)
        R_inv = np.array([[cp, sp, 0], [-sp, cp, 0], [0, 0, 1]])

        # Transformation matrix
        A = T @ R_inv @ np.linalg.inv(T)

        new_x, new_y = h2e(
            A @ e2h(np.array([self.l_arm.pos.x, self.l_arm.pos.y])))
        self.l_arm.pos.move(x=new_x, y=new_y)

        new_x, new_y = h2e(
            A @ e2h(np.array([self.r_arm.pos.x, self.r_arm.pos.y])))
        self.r_arm.pos.move(x=new_x, y=new_y)


class Arm(BasisObject):
    def __init__(self, mid: Position, skin_color, sleeve_color,
                 start_x=0, start_y=0, start_z=0,
                 rot_x=0, rot_y=0, rot_z=0,
                 is_left=True):
        self.mid = mid

        side = "L" if is_left else "R"
        mtl_images = {"skin": skin_color, "sleeve": sleeve_color}

        super().__init__(f"arm{side}", CHARACTER_FOLDER,
                         mid.x + start_x,
                         mid.y + start_y,
                         mid.z + start_z,
                         mid.rx + rot_x,
                         mid.ry + rot_y,
                         mid.rz + rot_z,
                         mtl_images)


class Legs:
    def __init__(self, mid: Position, pants_color, shoes_color,
                 start_x=0, start_y=0, start_z=0,
                 rot_x=0, rot_y=0, rot_z=0):
        self.mid = mid

        self.pos = Position(start_x, start_y, start_z,
                            rot_x, rot_y, rot_z)

        self.l_leg = Leg(mid, pants_color, shoes_color,
                         start_x, start_y, start_z,
                         rot_x, rot_y, rot_z,
                         is_left=True)

        self.r_leg = Leg(mid, pants_color, shoes_color,
                         start_x, start_y, start_z,
                         rot_x, rot_y, rot_z,
                         is_left=False)

    def generate(self):
        for o in [self.l_leg, self.r_leg]:
            o.generate()

    def render(self):
        for o in [self.l_leg, self.r_leg]:
            o.render()

    def move_delta(self, dx=0, dy=0, dz=0):
        self.l_leg.move_delta(dx, dy, dz)
        self.r_leg.move_delta(dx, dy, dz)
        self.pos.move_delta(dx, dy, dz)

    def rotate_delta(self, dx=0, dy=0, dz=0):
        self.l_leg.rotate_delta(dx, dy, dz)
        self.r_leg.rotate_delta(dx, dy, dz)
        self.pos.rotate_delta(dx, dy, dz)

        if not dy:
            return

        return

        # Translation matrix
        T = np.array(
            [[1, 0, self.mid.x], [0, 1, self.mid.y], [0, 0, 1]])

        # Rotation matrix
        phi = np.radians(dy)
        cp = np.cos(-phi)
        sp = np.sin(-phi)
        R_inv = np.array([[cp, sp, 0], [-sp, cp, 0], [0, 0, 1]])

        # Transformation matrix
        A = T @ R_inv @  np.linalg.inv(T)

        # Rotate around mid to move the left leg
        new_x, new_y = h2e(
            A @ e2h(np.array([self.l_leg.pos.x, self.l_leg.pos.y])))
        self.l_leg.pos.move(x=new_x, y=new_y)

        # Rotate around mid to move the right leg
        new_x, new_y = h2e(
            A @ e2h(np.array([self.r_leg.pos.x, self.r_leg.pos.y])))
        self.r_leg.pos.move(x=new_x, y=new_y)


class Leg(BasisObject):
    def __init__(self, mid, pants_color, shoes_color,
                 start_x=0, start_y=0, start_z=0,
                 rot_x=0, rot_y=0, rot_z=0,
                 is_left: bool = True):
        self.mid = mid
        self.extra_rot = 0

        side = "L" if is_left else "R"

        mtl_images = {"pants": pants_color, "shoes": shoes_color}

        super().__init__(f"leg{side}", CHARACTER_FOLDER,
                         mid.x + start_x,
                         mid.y + start_y,
                         mid.z + start_z,
                         mid.rx + rot_x,
                         mid.ry + rot_y,
                         mid.rz + rot_z,
                         mtl_images)

    def change_pants_color(self, color):
        mtl_images = {"pants": color}
        self.object.change_img(mtl_images, CHARACTER_FOLDER)

    def render(self):
        self.object.render(self.pos, extra_rot=self.extra_rot)
