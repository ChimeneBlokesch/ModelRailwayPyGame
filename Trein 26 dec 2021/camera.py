import numpy as np
import pygame
import math
from constants import Punt
import OpenGL.GL as GL
import OpenGL.GLU as GLU
from constants import print_rails_info, show_coordinates

MOVE_STEP = 0.05
ROTATE_STEP = 1

CAMERA_FREE = 0
CAMERA_POPPETJE = 1
CAMERA_TREIN = 2


class Camera:
    def __init__(self):
        self.pos = Punt(0, 1.5, -1.5)
        self.rotate_pos = Punt(0, 283, 0)  # (0, 0) is bovenaanzicht
        self.scale = 0
        self.mode = CAMERA_FREE

        # Poppetje mode
        self.distance_from_player = -2
        self.pitch = 45
        self.angle = 0
        self.object = None
        self.yaw = 0

    def move(self, x=None, y=None, z=None):
        x = x if x is not None else self.pos.x
        y = y if y is not None else self.pos.y
        z = z if z is not None else self.pos.z

        self.pos = Punt(x, y, z)

    def move_delta(self, dx=0, dy=0, dz=0):
        self.move(self.pos.x + dx, self.pos.y + dy, self.pos.z + dz)

    def rotate_delta(self, dx=0, dy=0, dz=0):
        self.rotate((self.rotate_pos.x + dx) % 360,
                    (self.rotate_pos.y + dy) % 360,
                    (self.rotate_pos.z + dz) % 360)

    def rotate(self, x=None, y=None, z=None):
        x = x if x is not None else self.rotate_pos.x
        y = y if y is not None else self.rotate_pos.y
        z = z if z is not None else self.rotate_pos.z

        self.rotate_pos = Punt(x, y, z)

    def free_camera(self, keys):
        SPEEDUP_STEP = 1 + 2 * keys[pygame.K_RSHIFT]
        tx, ty, tz = (0, 0, 0)
        rx, ry, rz = (0, 0, 0)

        # Move to left or right
        tx += SPEEDUP_STEP * MOVE_STEP * \
            (keys[pygame.K_LEFT] - keys[pygame.K_RIGHT]) * \
            math.cos(math.radians(self.rotate_pos.z))

        ty += SPEEDUP_STEP * MOVE_STEP * \
            (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * \
            math.sin(math.radians(self.rotate_pos.z))

        # Rotate around point of grid
        rz += SPEEDUP_STEP * ROTATE_STEP * \
            (keys[pygame.K_COMMA] - keys[pygame.K_PERIOD])

        # Move further, back
        if not keys[pygame.K_LCTRL]:
            ty += SPEEDUP_STEP * 0.5 * MOVE_STEP * \
                (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * \
                math.cos(math.radians(self.rotate_pos.z))

            tx += SPEEDUP_STEP * 0.5 * MOVE_STEP * \
                (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * \
                math.sin(math.radians(self.rotate_pos.z))

        # Move up or down
        tz += SPEEDUP_STEP * 2 * MOVE_STEP * \
            (keys[pygame.K_PAGEUP] - keys[pygame.K_PAGEDOWN])

        # Rotate up or down
        ry += SPEEDUP_STEP * ROTATE_STEP * keys[pygame.K_LCTRL] * \
            (keys[pygame.K_UP] - keys[pygame.K_DOWN])

        self.move_delta(tx, ty, tz)
        self.rotate_delta(rx, ry, rz)

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
        theta = -self.object.rotate_pos.y + self.angle
        offset_x = horizontal * math.sin(math.radians(theta))
        offset_y = horizontal * math.cos(math.radians(theta))
        temp_old_pos = self.pos
        self.move(x=-self.object.pos.x + offset_x,
                  y=-self.object.pos.y + offset_y,
                  z=-self.object.pos.z + vertical)

        # Yaw
        self.yaw = (-180 + theta) % 360
        self.rotate(z=self.yaw)

        if not np.allclose(temp_old_pos, self.pos):
            print("Camera", *self.pos, *self.rotate_pos)

    def render(self, keys):
        # TODO When playing as Pepper, rotate around pepper.pos, by using
        # sinus and cosinus to have new x and y.

        if self.mode == CAMERA_POPPETJE or self.mode == CAMERA_TREIN:
            return self.poppetje_camera(keys)

        return self.free_camera(keys)

    def camera_to_poppetje(self, pop):
        self.mode = CAMERA_POPPETJE
        self.object = pop

    def camera_to_trein(self, trein):
        self.mode = CAMERA_TREIN
        self.object = trein

    def camera_to_free(self):
        self.mode = CAMERA_FREE
        self.object = None
