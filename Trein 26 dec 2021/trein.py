from position import Position
from rails import RAILS_BOCHT, RAILS_RECHT
import math
from objparser import Object3D

from constants import SPEEDUP_BOCHT, TREINEN_MAP, afstand

# These indices correspond with the primary keys of the 'type' table.
TREIN_PASSAGIER = 0
TREIN_GOEDEREN = 1
TREIN_LOCOMOTIEF = 2


class Trein:
    def __init__(self, name, obj_name, type_trein, start_x=0, start_y=0,
                 start_z=0, rot_x=0, rot_y=0, rot_z=0, mtl_images=None):
        self.name = name
        self.obj_name = obj_name
        self.mtl_images = mtl_images
        self.object = self.create_object()
        self.start_angle = 0
        self.speed = 0
        self.pos = Position(start_x, start_y, start_z, rot_x, rot_y, rot_z)
        self.rails = None
        self.trein_next = None

        # Locomotief, passagier, goederen
        self.type = type_trein

    def create_object(self):
        model = Object3D(TREINEN_MAP, self.obj_name)

        if self.mtl_images:
            model.change_img(self.mtl_images, TREINEN_MAP)

        return model

    def generate(self):
        self.object.generate()

    def render(self):
        if self.name.startswith("VIRM"):
            self.object.render(self.pos, scale_value=(2, 0.7, 0.7))
            return

        if self.name.startswith("Loco"):
            self.object.render(self.pos, scale_value=(2, 1, 1.5))
            return

        self.object.render(self.pos)

    def rijden(self):
        if self.rails is None:
            return

        # TODO:
        # Als er een trein meerdere wagons heeft, deze wagons snelheid
        # van locomotief geven. Hiervoor is grid nodig om
        # locomotieven eerst te berekenen.

        # TODO: change to begin-/endpoint
        if self.speed < 0 and afstand(*self.rails.ref_punt_next, *self.
                                      pos.get_x_y()) < abs(self.speed):
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
                                        pos.get_x_y()) < abs(self.speed):
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

            # Direction is -1 or 1, depending on it goes right/up or left/down.
            direction = ((self.rails.go_left_down-1) **
                         1 + self.rails.go_left_down | 0)

            # The increase of the position.
            direction *= self.speed

            if self.rails.get_rotation() == 0:
                # Horizontal
                self.pos.move_delta(dx=direction)
            elif self.rails.get_rotation() == 90:
                # Vertical
                self.pos.move_delta(dy=direction)

        elif self.rails.type == RAILS_BOCHT:
            rotation = self.pos.ry + SPEEDUP_BOCHT * self.speed
            self.pos.rotate(y=rotation)

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

            self.pos.move(x=round(width * math.cos(rotation) + pos_x, 2),
                          y=round(height * math.sin(rotation) + pos_y, 2))

        # Change speed of train behind it
        # if self.trein_next:
        #     self.trein_next.change_speed(-self.speed)

    def change_speed(self, speed):
        self.speed = -speed

    def attach_trein(self, trein=None):
        # Also possible to deattach trein
        self.trein_next = trein

        # Change speed to own speed
        if trein:
            self.trein_next.change_speed(-self.speed)
