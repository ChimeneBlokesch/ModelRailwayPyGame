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
        self.pos = Punt(0, 0, 15)
        self.rotate_pos = Punt(0, -90, 0)  # (0, 0) is bovenaanzicht
        self.scale = 0

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

    def render(self, keys):
        SPEEDUP_STEP = 1 + 2 * keys[pygame.K_RSHIFT]
        tx, ty, tz = self.pos
        rx, ry, rz = self.rotate_pos

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
        tz += SPEEDUP_STEP * MOVE_STEP * \
            (keys[pygame.K_PAGEUP] - keys[pygame.K_PAGEDOWN])

        # Rotate up or down
        ry += SPEEDUP_STEP * ROTATE_STEP * keys[pygame.K_LCTRL] * \
            (keys[pygame.K_UP] - keys[pygame.K_DOWN])

        self.move(tx, ty, tz)

        rx = rx % 360
        ry = ry % 360
        rz = rz % 360

        self.rotate(rx, ry, rz)

        self.scale += SPEEDUP_STEP * \
            (keys[pygame.K_z] - keys[pygame.K_x]) * 0.05
