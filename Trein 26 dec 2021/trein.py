from rails import RAILS_BOCHT, RAILS_RECHT
import math
from objparser import Object3D

from constants import SPEEDUP_BOCHT, Punt, TREINEN_MAP, afstand


class Trein:
    def __init__(self, name, obj_name, mid_x, mid_y, mtl_images=None):
        self.name = name
        self.obj_name = obj_name
        self.mtl_images = mtl_images
        self.object = self.create_object()
        self.start_angle = 0
        self.speed = 0
        self.rotate_pos = Punt(0, 0, 0)
        self.pos = Punt(0, 0, 0)
        self.mid = (mid_x, mid_y)
        self.rails = None

    def create_object(self):
        model = Object3D(TREINEN_MAP, self.obj_name)

        if self.mtl_images:
            model.change_img(self.mtl_images)

        return model

    def generate(self):
        self.object.generate()

    def render(self):
        if self.name.startswith("VIRM"):
            self.object.render(self.pos, self.rotate_pos,
                               scale_value=(2, 0.7, 0.7))
            return

        if self.name.startswith("Loco"):
            self.object.render(self.pos, self.rotate_pos,
                               scale_value=(2, 1, 1.5))
            return

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

    def rijden(self):
        if self.rails is None:
            return

        # TODO: change to begin-/endpoint
        if self.speed < 0 and afstand(*self.rails.ref_punt_next, *self.
                                      pos[:2]) < abs(self.speed):
            # print("Next rails")
            if not self.rails.next:
                # End of rail, go in opposite direction.
                self.change_speed(self.speed)
            elif self.rails.type == RAILS_BOCHT and \
                    self.rails.next.type == RAILS_BOCHT and \
                    self.rails.own_next_prev != self.rails.next.own_next_prev:
                # These two rails belong to each other so the other rails can
                # be ignored.
                if not self.rails.next.next:
                    self.change_speed(self.speed)
                else:
                    self.rails = self.rails.next.next
            else:
                self.rails = self.rails.next
        elif self.speed > 0 and afstand(*self.rails.ref_punt_prev, *self.
                                        pos[:2]) < abs(self.speed):
            # print("Prev rails")
            if not self.rails.prev:
                # End of rail, go in opposite direction.
                self.change_speed(self.speed)
            elif self.rails.type == RAILS_BOCHT and \
                    self.rails.prev.type == RAILS_BOCHT and \
                    self.rails.own_next_prev != self.rails.prev.own_next_prev:
                # These two rails belong to each other so the other rails can
                # be ignored.
                if not self.rails.prev.prev:
                    self.change_speed(self.speed)
                else:
                    self.rails = self.rails.prev.prev
            else:
                self.rails = self.rails.prev

        # Depending on rails.angle the train rotates
        if self.rails.type == RAILS_RECHT:
            # 0 of 180
            TEMP_SCALE = 100
            old_mid_x, old_mid_y = self.mid
            old_mid_x *= TEMP_SCALE
            old_mid_y *= TEMP_SCALE

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

                self.mid = (round((old_mid_x+direction * TEMP_SCALE) /
                                  TEMP_SCALE, 2),
                            round(old_mid_y / TEMP_SCALE, 2))
            elif self.rails.rotation == 90:
                # Vertical
                self.move(y=direction + self.pos.y)
                self.mid = (round(old_mid_x / TEMP_SCALE, 2),
                            round((old_mid_y + direction * TEMP_SCALE) /
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

            self.mid = (round(width * math.cos(rotation) + pos_x, 2),
                        round(height * math.sin(rotation) + pos_y, 2))

            self.move(x=round(width * math.cos(rotation) + pos_x, 2),
                      y=round(height * math.sin(rotation) + pos_y, 2))

    def change_speed(self, speed):
        self.speed = -speed
