from rails import RAILS_BOCHT, RAILS_RECHT
import math
from objparser import Object3D

from constants import SPEEDUP_BOCHT, Punt, TREINEN_MAP, afstand


class Trein:
    def __init__(self, name, filename, x, y):
        self.name = name
        self.path_to_obj_file = TREINEN_MAP + filename
        self.object = self.create_object()
        self.start_angle = 0
        self.speed = 0
        self.rotate_pos = Punt(0, 0, 0)
        self.pos = Punt(0, 0, 0)
        self.ref_punt = (x, y)

    def create_object(self):
        return Object3D(self.path_to_obj_file)

    def generate(self):
        self.object.generate()

    def render(self):
        self.object.render(self.pos, self.rotate_pos)

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

    def get_ref_punt(self):
        return self.ref_punt

    def rijden(self):
        if afstand(*self.rails.ref_punt_next, *self.ref_punt) < 0.05:
            print("Next rails")
            self.rails = self.rails.next

        # Depending on rails.angle the train rotates
        if self.rails.type == RAILS_RECHT:
            # 0 of 180
            old_x, old_y = self.ref_punt
            TEMP_SCALE = 100
            old_x *= TEMP_SCALE
            old_y *= TEMP_SCALE

            # Direction is -1 or 1, depending on it goes right/up or left/down.
            direction = ((self.rails.go_left_down-1) **
                         1 + self.rails.go_left_down | 0)

            # The increase of the position.
            direction *= self.speed

            if self.rails.rotation == 0:
                # Horizontal
                self.move(x=direction + self.pos.x)
                # self.ref_punt = ((old_x + direction * TEMP_SCALE)
                #                  / TEMP_SCALE,
                #                  old_y / TEMP_SCALE)

                self.ref_punt = (round((old_x+direction * TEMP_SCALE) /
                                       TEMP_SCALE, 2),
                                 round(old_y / TEMP_SCALE, 2))
            elif self.rails.rotation == 90:
                # Vertical
                self.move(y=direction + self.pos.y)
                self.ref_punt = (round(old_x / TEMP_SCALE, 2),
                                 round((old_y + direction * TEMP_SCALE) /
                                 TEMP_SCALE, 2))
        elif self.rails.type == RAILS_BOCHT:
            rotation = self.rotate_pos.y + SPEEDUP_BOCHT * self.speed
            self.rotate(y=rotation)

            width = abs(
                self.rails.ref_punt_prev[0] - self.rails.ref_punt_next[0])
            height = abs(
                self.rails.ref_punt_prev[1] - self.rails.ref_punt_next[1])

            if self.rails.relative_rotation in [90, 135, 180, 225]:
                if max(self.rails.ref_punt_prev[1], self.rails.ref_punt_next[1]
                       ) == self.rails.ref_punt_next[1]:
                    pos_x = self.rails.ref_punt_next[0]
                    pos_y = self.rails.ref_punt_prev[1]
                else:
                    pos_x = self.rails.ref_punt_prev[0]
                    pos_y = self.rails.ref_punt_next[1]
            else:
                if min(self.rails.ref_punt_prev[1],
                       self.rails.ref_punt_next[1]
                       ) == self.rails.ref_punt_next[1]:
                    pos_x = self.rails.ref_punt_next[0]
                    pos_y = self.rails.ref_punt_prev[1]
                else:
                    pos_x = self.rails.ref_punt_prev[0]
                    pos_y = self.rails.ref_punt_next[1]

            rotation = math.radians(rotation)

            self.ref_punt = (round(width * math.cos(rotation) + pos_x, 2),
                             round(height * math.sin(rotation) + pos_y, 2))

            self.move(x=round(width * math.cos(rotation) + pos_x, 2),
                      y=round(height * math.sin(rotation) + pos_y, 2))

    def change_speed(self, speed):
        self.speed = -speed
