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


class Camera:
    def __init__(self):
        self.pos = Punt(0, 1.5, -1.5)
        self.rotate_pos = Punt(0, 283, 0)  # (0, 0) is bovenaanzicht
        self.scale = 0
        self.mode = CAMERA_FREE

        # Poppetje mode
        self.distance_from_player = -3
        self.pitch = 45
        self.angle = 0
        self.poppetje = None
        self.yaw = 0

    def move(self, x=None, y=None, z=None):
        x = x if x is not None else self.pos.x
        y = y if y is not None else self.pos.y
        z = z if z is not None else self.pos.z

        self.pos = Punt(x, y, z)

    def move_delta(self, dx=0, dy=0, dz=0):
        self.move(self.pos.x + dx, self.pos.y + dy, self.pos.z + dz)

    def rotate_delta(self, dx=0, dy=0, dz=0):
        self.rotate(self.rotate_pos.x + dx,
                    self.rotate_pos.y + dy,
                    self.rotate_pos.z + dz)

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
            math.cos(math.radians(rz))

        ty += SPEEDUP_STEP * MOVE_STEP * \
            (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * \
            math.sin(math.radians(rz))

        # Rotate around point of grid
        rz += SPEEDUP_STEP * ROTATE_STEP * \
            (keys[pygame.K_COMMA] - keys[pygame.K_PERIOD])

        # Move further, back
        if not keys[pygame.K_LCTRL]:
            ty += SPEEDUP_STEP * 0.5 * MOVE_STEP * \
                (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * \
                math.cos(math.radians(rz))

            tx += SPEEDUP_STEP * 0.5 * MOVE_STEP * \
                (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * \
                math.sin(math.radians(rz))

        # Move up or down
        tz += SPEEDUP_STEP * 2 * MOVE_STEP * \
            (keys[pygame.K_PAGEUP] - keys[pygame.K_PAGEDOWN])

        # Rotate up or down
        ry += SPEEDUP_STEP * ROTATE_STEP * keys[pygame.K_LCTRL] * \
            (keys[pygame.K_UP] - keys[pygame.K_DOWN])

        # if self.mode == CAMERA_POPPETJE:
        #     # Rotate around poppetje.
        #     # if keys[pygame.K_COMMA] or keys[pygame.K_PERIOD]:
        #     #     tx += ...
        #     GLU.gluLookAt()

        self.move(self.pos[0] + tx, self.pos[1] + ty, self.pos[2] + tz)

        self.rotate((self.rotate_pos[0] + rx) % 360,
                    (self.rotate_pos[1] + ry) % 360,
                    (self.rotate_pos[2] + rz) % 360)

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
        theta = self.poppetje.rotate_pos.y + self.angle
        offset_x = horizontal * math.sin(math.radians(theta))
        offset_y = horizontal * math.cos(math.radians(theta))
        self.move(x=self.poppetje.pos.x + offset_x,
                  y=self.poppetje.pos.y + offset_y,
                  z=self.poppetje.pos.z + vertical)

        # Yaw
        self.yaw = ((self.poppetje.rotate_pos.y + self.angle) - 180) % 360
        self.rotate(x=self.yaw)

        return (-1, -1, -1), (-1, -1, -1)  # TODO: maybe not needed anymore

    def render(self, keys):
        # TODO When playing as Pepper, rotate around pepper.pos, by using
        # sinus and cosinus to have new x and y.

        if self.mode == CAMERA_FREE:
            return self.free_camera(keys)

        return self.poppetje_camera(keys)

    def camera_to_poppetje(self, pop):
        self.mode = CAMERA_POPPETJE
        self.poppetje = pop

    def camera_to_free(self):
        self.mode = CAMERA_FREE
        self.poppetje = None
