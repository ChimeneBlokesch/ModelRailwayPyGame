import pygame
import math
from position import Position

MOVE_STEP = 0.05
ROTATE_STEP = 1

CAMERA_FREE = 0
CAMERA_POPPETJE = 1
CAMERA_TRAIN = 2


class Camera:
    def __init__(self):
        self.pos = Position(x=0, y=1.5, z=-1.5, rx=0, ry=283, rz=0)
        self.scale = 0
        self.mode = CAMERA_FREE

        # Poppetje mode
        self.distance_from_player = -2
        self.pitch = 45
        self.angle = 0
        self.object = None
        self.yaw = 0

    def free_camera(self, keys):
        SPEEDUP_STEP = 1 + 2 * keys[pygame.K_RSHIFT]
        tx, ty, tz = (0, 0, 0)
        rx, ry, rz = (0, 0, 0)

        # Move to left or right
        tx += SPEEDUP_STEP * MOVE_STEP * \
            (keys[pygame.K_LEFT] - keys[pygame.K_RIGHT]) * \
            math.cos(math.radians(self.pos.rz))

        ty += SPEEDUP_STEP * MOVE_STEP * \
            (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * \
            math.sin(math.radians(self.pos.rz))

        # Rotate around point of grid
        rz += SPEEDUP_STEP * ROTATE_STEP * \
            (keys[pygame.K_COMMA] - keys[pygame.K_PERIOD])

        # Move further, back
        if not keys[pygame.K_LCTRL]:
            ty += SPEEDUP_STEP * 0.5 * MOVE_STEP * \
                (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * \
                math.cos(math.radians(self.pos.rz))

            tx += SPEEDUP_STEP * 0.5 * MOVE_STEP * \
                (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * \
                math.sin(math.radians(self.pos.rz))

        # Move up or down
        tz += SPEEDUP_STEP * 2 * MOVE_STEP * \
            (keys[pygame.K_PAGEUP] - keys[pygame.K_PAGEDOWN])

        # Rotate up or down
        ry += SPEEDUP_STEP * ROTATE_STEP * keys[pygame.K_LCTRL] * \
            (keys[pygame.K_UP] - keys[pygame.K_DOWN])

        self.pos.move_delta(tx, ty, tz)
        self.pos.rotate_delta(rx, ry, rz)

        # TODO: kijken of move en rotate afhangen van scale
        self.scale += SPEEDUP_STEP * \
            (keys[pygame.K_z] - keys[pygame.K_x]) * 0.05

        return (tx, ty, tz), (rx, ry, rz)

    def poppetje_camera(self, keys):
        SPEEDUP_STEP = 1 + 2 * keys[pygame.K_RSHIFT]
        # zoom
        zoomlevel = SPEEDUP_STEP * (keys[pygame.K_z] - keys[pygame.K_x]) * 0.05
        self.distance_from_player -= zoomlevel

        # pitch
        d_pitch = SPEEDUP_STEP * keys[pygame.K_LCTRL] * \
            (keys[pygame.K_UP] - keys[pygame.K_DOWN]) * 0.5
        self.pitch -= d_pitch

        # angle
        d_angle = SPEEDUP_STEP * (keys[pygame.K_COMMA] - keys[pygame.K_PERIOD])
        self.angle += d_angle

        # Horizontal and vertical distance
        horizontal = self.distance_from_player * \
            math.cos(math.radians(self.pitch))
        vertical = self.distance_from_player * \
            math.sin(math.radians(self.pitch))

        # Camera position
        theta = -self.object.pos.ry + self.angle
        offset_x = horizontal * math.sin(math.radians(theta))
        offset_y = horizontal * math.cos(math.radians(theta))
        temp_old_pos = self.pos
        self.pos.move(x=-self.object.pos.x + offset_x,
                      y=-self.object.pos.y + offset_y,
                      z=-self.object.pos.z + vertical)

        # Yaw
        self.yaw = (-180 + theta) % 360
        self.pos.rotate(z=self.yaw)

        if not temp_old_pos.is_equal(self.pos):
            print("Camera", *self.pos.get_pos(), *self.pos.get_rotate())

    def render(self, keys):
        if self.mode == CAMERA_POPPETJE or self.mode == CAMERA_TRAIN:
            return self.poppetje_camera(keys)

        return self.free_camera(keys)

    def camera_to_poppetje(self, pop):
        self.mode = CAMERA_POPPETJE
        self.object = pop

    def camera_to_train(self, train):
        self.mode = CAMERA_TRAIN
        self.object = train

    def camera_to_free(self):
        self.mode = CAMERA_FREE
        self.object = None
