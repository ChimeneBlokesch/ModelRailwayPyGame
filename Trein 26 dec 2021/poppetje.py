import math
import numpy as np
import pygame
from basis_object import BasisObject
from objparser import Object3D


from constants import POPPETJES_MAP, SPEEDUP_BOCHT, TREINEN_MAP, afstand, e2h, h2e
from position import Position

RUN_SPEED = 0.1
WALK_SPEED = RUN_SPEED / 2
ROTATE_SPEED = 1.5
JUMP_SPEED = 0.1
GRAVITY = -0.01
TERRAIN_HEIGHT = 0

RUN_SPEED2 = 10
WALK_SPEED2 = RUN_SPEED2 / 2


# TODO: put in constants.py
POPPETJES2_MAP = "Poppetjes2/"

HAND_COLOR = (0.991102, 0.708376, 0.000000)
BB_HAND_COLOR = (0.3, 0.3, 0.3)  # TODO another color

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
    def __init__(self, name, hat_hair, hat_hair_color, face,
                 trui_color, trui_voor, mouw, riem, broek, broek_midden,
                 start_x=0, start_y=0, start_z=0,
                 rot_x=0, rot_y=0, rot_z=0, is_brickbot=False):
        """
        Colors should be given as the tuple (r, g, b) and not gamma corrected.
        """
        self.name = name
        self.direction = 100
        self.speed = 0  # 5
        self.start_angle = 0
        self.turn_speed = 0
        self.up_speed = 0

        self.is_player = False
        self.jump_level = 0  # 0: on ground, 1: small jump, 2: big jump
        self.pos = Position(start_x, start_y, start_z, rot_x, rot_y, rot_z)
        self.hathair = HatHair(hat_hair, hat_hair_color, start_x,
                               start_y, start_z, rot_x, rot_y, rot_z)
        self.head = Head(face, start_x, start_y,
                         start_z, rot_x, rot_y, rot_z, is_brickbot=is_brickbot)
        self.trui = Trui(self.pos, trui_color, trui_voor, start_x,
                         start_y, start_z, rot_x, rot_y, rot_z)
        self.arms = Arms(mouw, start_x, start_y, start_z, rot_x, rot_y, rot_z,
                         is_brickbot=is_brickbot)
        self.legs = Legs(riem, broek, broek_midden,
                         start_x, start_y, start_z, rot_x, rot_y, rot_z)
        self.objects = [self.hathair, self.head,
                        self.trui, self.arms, self.legs]

    def generate(self):
        for o in self.objects:
            o.generate()

    def render(self):
        self.move_legs()

        for o in self.objects:
            o.render()

    def move_legs(self):
        if self.legs.l_leg.pos.rx > 160 or self.legs.r_leg.pos.rx > 160:
            self.direction *= -1

        self.legs.l_leg.pos.rotate_delta(dx=self.direction * self.speed)
        self.legs.r_leg.pos.rotate_delta(dx=-self.direction * self.speed)

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

        # if distance or self.turn_speed:
        #     print("Pepper", *
        #           (self.pos.get_pos()), *(self.get_rotate()))

        self.move_delta(dx=dx, dy=dy)

        dz = (self.up_speed)
        self.move_delta(dz=dz)

        if self.legs.l_leg.pos.z < TERRAIN_HEIGHT:
            self.up_speed = 0
            dz = -self.legs.l_leg.pos.z
            self.move_delta(dz=dz)
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


class HatHair(BasisObject):
    def __init__(self, obj, color, start_x=0, start_y=0, start_z=0, rot_x=0, rot_y=0, rot_z=0):
        # Color (r, g, b)
        # start_y += 0.013754
        # start_z += 0.226  # 0.08  # offset
        start_z += 0.253014
        mtl_images = {"hathair": color}
        super().__init__(obj, POPPETJES2_MAP, start_x, start_y,
                         start_z, rot_x, rot_y, rot_z, mtl_images)

    def change_color(self, color):
        mtl_images = {"hathair": color}
        self.object.change_img(mtl_images, POPPETJES2_MAP)


class Head(BasisObject):
    def __init__(self, face_name, start_x=0, start_y=0, start_z=0, rot_x=0, rot_y=0, rot_z=0, is_brickbot=False):
        self.face_name = face_name
        mtl_images = {"face": ["face\\" + face_name + "_face" + "0" + ".png"]}
        # start_y += 0.008933
        # start_z += 0.206643  # 0.1  # offset
        start_z += 0.206643
        super().__init__("head", POPPETJES2_MAP, start_x, start_y,
                         start_z, rot_x, rot_y, rot_z, mtl_images)

    def change_emotion(self, num):
        mtl_images = {"face": ["face\\" + self.face_name + str(num) + ".png"]}
        self.object.change_img(mtl_images, POPPETJES2_MAP)

    def change_face(self, face_name, num=0):
        self.face_name = face_name
        mtl_images = {"face": ["face\\" + self.face_name + str(num) + ".png"]}
        self.object.change_img(mtl_images, POPPETJES2_MAP)


class Trui(BasisObject):
    def __init__(self, mid, trui_color, trui_voor, start_x=0, start_y=0, start_z=0, rot_x=0, rot_y=0, rot_z=0):
        self.mid = mid
        self.trui_color = trui_color
        mtl_images = {"trui": trui_color,
                      "trui_voor": ["trui_voor\\" + trui_voor + "_trui_voor.png"]}
        # offset
        # start_x += -0.000595
        # start_y += 0.011617
        # start_z += 0.096093
        start_z += 0.096093
        super().__init__("trui", POPPETJES2_MAP, start_x, start_y,
                         start_z, rot_x, rot_y, rot_z, mtl_images)

    def change_trui_voor(self, trui_voor):
        mtl_images = {"trui": ["trui_voor\\" + trui_voor + "_trui_voor.png"]}
        self.object.change_img(mtl_images, POPPETJES2_MAP)

    def change_trui_color(self, color):
        mtl_images = {"trui": color}
        self.object.change_img(mtl_images, POPPETJES2_MAP)

    def rotate_delta(self, dx=0, dy=0, dz=0):
        super().rotate_delta(dx, dy, dz)

        if dy:
            T = np.array(
                [[1, 0, self.mid.x], [0, 1, self.mid.y], [0, 0, 1]])
            print("T", T)
            phi = dy

            cp = np.cos(-phi)
            sp = np.sin(-phi)
            R_inv = np.array([[cp, -sp, 0], [sp, cp, 0], [0, 0, 1]]).T
            print("R_inv", R_inv)
            R = np.array([[cp, -sp, 0], [sp, cp, 0], [0, 0, 1]])
            print("T @ R", T @ R)
            print("R @ np.linalg.inv(T)", R @ np.linalg.inv(T))
            A = T @ R_inv @  np.linalg.inv(T)
            print("A", A)
            new_x, new_y = h2e(
                A @ e2h(np.array([self.pos.x, self.pos.y])))
            self.pos.move(x=new_x, y=new_y)


class Arms:
    def __init__(self, mouw, start_x=0,
                 start_y=0, start_z=0, rot_x=0, rot_y=0, rot_z=0,
                 is_brickbot=False):
        self.pos = Position(start_x, start_y, start_z, rot_x, rot_y, rot_z)
        self.l_arm = Arm(mouw, True,
                         start_x, start_y, start_z, rot_x, rot_y, rot_z)
        self.r_arm = Arm(mouw, False,
                         start_x, start_y, start_z, rot_x, rot_y, rot_z)
        self.l_hand = Hand(True,
                           start_x, start_y, start_z, rot_x, rot_y, rot_z,
                           is_brickbot=is_brickbot)
        self.r_hand = Hand(False,
                           start_x, start_y, start_z, rot_x, rot_y, rot_z,
                           is_brickbot=is_brickbot)

    def generate(self):
        for o in [self.l_arm, self.r_arm, self.l_hand, self.r_hand]:
            o.generate()

    def render(self):
        for o in [self.l_arm, self.l_hand, self.r_hand]:
            o.render()

    def move_delta(self, dx=0, dy=0, dz=0):
        self.pos.move_delta(dx, dy, dz)
        self.l_arm.move_delta(dx, dy, dz)
        self.r_arm.move_delta(dx, dy, dz)
        self.l_hand.move_delta(dx, dy, dz)
        self.r_hand.move_delta(dx, dy, dz)

    def rotate_delta(self, dx=0, dy=0, dz=0):
        self.pos.rotate_delta(dx, dy, dz)
        self.l_arm.rotate_delta(dx, dy, dz)
        self.r_arm.rotate_delta(dx, dy, dz)
        self.l_hand.rotate_delta(dx, dy, dz)
        self.r_hand.rotate_delta(dx, dy, dz)

        if dy:  # Telkens 1.5
            print("dy", dy)
            print("self.pos", self.pos.get_pos(), self.pos.get_rotate())
            print("l_arm", self.l_arm.pos.get_pos(),
                  self.l_arm.pos.get_rotate())
            T = np.array(
                [[1, 0, self.pos.x], [0, 1, self.pos.y], [0, 0, 1]])
            print("T", T)
            print("T @ mid", T @ e2h(np.array([self.pos.x, self.pos.y])))
            phi = dy

            cp = np.cos(-phi)
            sp = np.sin(-phi)
            R_inv = np.array([[cp, -sp, 0], [sp, cp, 0], [0, 0, 1]]).T
            print("R_inv", R_inv)
            R = np.array([[cp, -sp, 0], [sp, cp, 0], [0, 0, 1]])
            print("T @ R", T @ R)
            print("R @ np.linalg.inv(T)", R @ np.linalg.inv(T))
            A = T @ R_inv @  np.linalg.inv(T)
            print("A", A)
            new_x, new_y = h2e(
                A @ e2h(np.array([self.l_arm.pos.x, self.l_arm.pos.y])))
            radius = afstand(self.l_arm.pos.x, self.l_arm.pos.y,
                             self.pos.x,  self.pos.y)
            print("radius voor", radius)
            # new_x = radius * math.cos(math.radians(self.l_arm.pos.ry))
            # new_y = radius * math.sin(math.radians(self.l_arm.pos.ry))
            print(self.pos.x, self.pos.y, new_x, new_y)
            self.l_arm.pos.move(x=-new_x, y=new_y)
            radius = afstand(self.l_arm.pos.x, self.l_arm.pos.y,
                             self.pos.x,  self.pos.y)
            print("radius na", radius)

            # radius = afstand(self.r_arm.pos.x, self.r_arm.pos.y,
            #                  self.pos.x,  self.pos.y)
            # # new_x = radius * math.cos(math.radians(self.r_arm.pos.ry))
            # # new_y = radius * math.sin(math.radians(self.r_arm.pos.ry))
            # print(new_x, new_y)

            new_x, new_y = h2e(
                A @ e2h(np.array([self.r_arm.pos.x, self.r_arm.pos.y])))
            self.r_arm.pos.move(x=-new_x, y=new_y)


class Arm(BasisObject):
    def __init__(self, mouw, is_left,
                 start_x=0, start_y=0, start_z=0, rot_x=0, rot_y=0, rot_z=0):
        # offset
        # start_x += -0.048647 if not is_left else 0.046275  # 0.065608
        # # start_x += 0.0571275 * (2 * is_left - 1)
        # # start_y += 0.0087515
        # start_y += 0.00946 if not is_left else 0.014316  # 0.008043
        # start_z += 0.123011 if not is_left else 0.128958  # 0.105465
        # # start_z += 0.11424

        start_x += 0.046275 if is_left else -0.048647
        start_z += 0.128958 if is_left else 0.123011

        arm = "l" if is_left else "r"
        mtl_images = {"mouw": mouw}
        # start_z += 0.04  # offset
        super().__init__(arm + "_arm", POPPETJES2_MAP, start_x,
                         start_y, start_z, rot_x, rot_y, rot_z, mtl_images)


class Hand(BasisObject):
    def __init__(self, is_left,
                 start_x=0, start_y=0, start_z=0, rot_x=0, rot_y=0, rot_z=0,
                 is_brickbot=False):
        # offset
        # start_x += -0.076369 if not is_left else 0.082919
        # start_y += 0.000755 if not is_left else -0.001302
        # start_z += 0.064231 if not is_left else 0.055258
        # # start_x += 0.079644 * (2 * is_left)
        # # start_y += 0.0020385
        # # start_z += 0.3084055
        start_x += 0.082919 if is_left else -0.076369
        start_y += -0.014938 if is_left else -0.009387
        start_z += 0.055258 if is_left else 0.064231
        hand_color = HAND_COLOR if not is_brickbot else BB_HAND_COLOR
        obj = "hand" if not is_brickbot else "BB_hand"
        hand = "l" if is_left else "r"
        mtl_images = {"hand": hand_color}
        super().__init__(hand + "_" + obj, POPPETJES2_MAP,
                         start_x, start_y, start_z, rot_x, rot_y, rot_z,
                         mtl_images)


class Legs:
    def __init__(self, riem, broek, broek_midden,
                 start_x=0, start_y=0, start_z=0, rot_x=0, rot_y=0, rot_z=0):
        self.pos = Position(start_x, start_y, start_z, rot_x, rot_y, rot_z)
        self.between = Between(riem, broek_midden,
                               start_x, start_y, start_z, rot_x, rot_y, rot_z)
        self.l_leg = Leg(broek, True,
                         start_x, start_y, start_z, rot_x, rot_y, rot_z)

        self.r_leg = Leg(broek, False,
                         start_x, start_y, start_z, rot_x, rot_y, rot_z)

    def generate(self):
        for o in [self.between, self.l_leg, self.r_leg]:
            o.generate()

    def render(self):
        for o in [self.between, self.l_leg, self.r_leg]:
            o.render()

    def move_delta(self, dx=0, dy=0, dz=0):
        self.l_leg.move_delta(dx, dy, dz)
        self.r_leg.move_delta(dx, dy, dz)
        self.between.move_delta(dx, dy, dz)
        self.pos.move_delta(dx, dy, dz)

    def rotate_delta(self, dx=0, dy=0, dz=0):
        self.l_leg.rotate_delta(dx, dy, dz)
        self.r_leg.rotate_delta(dx, dy, dz)
        self.between.rotate_delta(dx, dy, dz)
        self.pos.rotate_delta(dx, dy, dz)


class Between(BasisObject):
    def __init__(self, riem, broek_midden, start_x=0, start_y=0, start_z=0, rot_x=0, rot_y=0, rot_z=0):
        mtl_images = {"riem": riem,
                      "broek_midden":  broek_midden}
        # offset
        # start_x -= 0.000075
        # start_y += 0.006344
        # start_z += 0.015503  # 0.01
        start_z += 0.015503

        super().__init__("between", POPPETJES2_MAP,
                         start_x, start_y, start_z, rot_x, rot_y, rot_z,
                         mtl_images)

    def change_riem(self, color):
        mtl_images = {"riem": color}
        self.object.change_img(mtl_images, POPPETJES2_MAP)

    def change_broek_midden(self, color):
        mtl_images = {"broek_midden": color}
        self.object.change_img(mtl_images, POPPETJES2_MAP)


class Leg(BasisObject):
    def __init__(self, color, is_left,
                 start_x=0, start_y=0, start_z=0, rot_x=0, rot_y=0, rot_z=0):
        # offset
        # start_x += -0.007519 if not is_left else 0.007519
        # start_y += 0.006783 if not is_left else 0.006783
        # # start_x += 0.00751 * (2 * is_left - 1)
        # # start_y += 0.006783 * (2 * is_left - 1)
        start_x += 0.007519 if is_left else -0.007519
        hand = "l" if is_left else "r"
        mtl_images = {"broek": color}
        super().__init__(hand + "_leg", POPPETJES2_MAP,
                         start_x, start_y, start_z, rot_x, rot_y, rot_z,
                         mtl_images)

    def change_color(self, color):
        mtl_images = {"broek": color}
        self.object.change_img(mtl_images, POPPETJES2_MAP)
