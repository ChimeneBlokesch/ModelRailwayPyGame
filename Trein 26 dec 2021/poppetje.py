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
        self.pos = Position(start_x, start_y, start_z, rot_x, rot_y, rot_z)
        self.hat = HatHair(hat_hair, hat_hair_color, start_x,
                           start_y, start_z, rot_x, rot_y, rot_z)
        self.head = Head(face, start_x, start_y,
                         start_z, rot_x, rot_y, rot_z, is_brickbot=is_brickbot)
        self.trui = Trui(trui_color, trui_voor, start_x,
                         start_y, start_z, rot_x, rot_y, rot_z)
        self.arms = Arms(mouw, start_x, start_y, start_z, rot_x, rot_y, rot_z,
                         is_brickbot=is_brickbot)
        self.legs = Legs(riem, broek, broek_midden,
                         start_x, start_y, start_z, rot_x, rot_y, rot_z)

    def generate(self):
        for o in [self.hat, self.head, self.trui, self.arms, self.legs]:
            o.generate()

    def render(self):
        for o in [self.hat, self.head, self.trui, self.arms, self.legs]:
            o.render()


class HatHair(BasisObject):
    def __init__(self, obj, color, start_x=0, start_y=0, start_z=0, rot_x=0, rot_y=0, rot_z=0):
        # Color (r, g, b)
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
        print(mtl_images)
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
    def __init__(self, trui_color, trui_voor, start_x=0, start_y=0, start_z=0, rot_x=0, rot_y=0, rot_z=0):
        self.trui_color = trui_color
        mtl_images = {"trui": trui_color,
                      "trui_voor": ["trui_voor\\" + trui_voor + "_trui_voor.png"]}
        super().__init__("trui", POPPETJES2_MAP, start_x, start_y,
                         start_z, rot_x, rot_y, rot_z, mtl_images)

    def change_trui_voor(self, trui_voor):
        mtl_images = {"trui": ["trui_voor\\" + trui_voor + "_trui_voor.png"]}
        self.object.change_img(mtl_images, POPPETJES2_MAP)

    def change_trui_color(self, color):
        mtl_images = {"trui": color}
        self.object.change_img(mtl_images, POPPETJES2_MAP)


class Arms:
    def __init__(self, mouw, start_x=0,
                 start_y=0, start_z=0, rot_x=0, rot_y=0, rot_z=0,
                 is_brickbot=False):
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
        for o in [self.l_arm, self.r_arm, self.l_hand, self.r_hand]:
            o.render()


class Arm(BasisObject):
    def __init__(self, mouw, is_left,
                 start_x=0, start_y=0, start_z=0, rot_x=0, rot_y=0, rot_z=0):
        arm = "l" if is_left else "r"
        mtl_images = {"mouw": mouw}
        super().__init__(arm + "_arm", POPPETJES2_MAP, start_x,
                         start_y, start_z, rot_x, rot_y, rot_z, mtl_images)


class Hand(BasisObject):
    def __init__(self, is_left,
                 start_x=0, start_y=0, start_z=0, rot_x=0, rot_y=0, rot_z=0,
                 is_brickbot=False):
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


class Between(BasisObject):
    def __init__(self, riem, broek_midden, start_x=0, start_y=0, start_z=0, rot_x=0, rot_y=0, rot_z=0):
        mtl_images = {"riem": riem,
                      "broek_midden":  broek_midden}
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
        hand = "l" if is_left else "r"
        mtl_images = {"broek": color}
        super().__init__(hand + "_leg", POPPETJES2_MAP,
                         start_x, start_y, start_z, rot_x, rot_y, rot_z,
                         mtl_images)

    def change_color(self, color):
        mtl_images = {"broek": color}
        self.object.change_img(mtl_images, POPPETJES2_MAP)
