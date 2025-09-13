from position import Position
from rails import RAILS_CURVE, RAILS_STRAIGHT
import math
from objparser import Object3D

from constants import SPEEDUP_CURVE, TRAINS_FOLDER, afstand

# These indices correspond with the primary keys of the 'type' table.
TRAIN_PASSENGER = 0
TRAIN_FREIGHT = 1
TRAIN_ENGINE = 2


class Train:
    def __init__(self, name, obj_name, type_train, start_x=0, start_y=0,
                 start_z=0, rot_x=0, rot_y=0, rot_z=0, mtl_images=None):
        self.name = name
        self.obj_name = obj_name
        self.mtl_images = mtl_images
        self.object = self.create_object()
        self.start_angle = 0
        self.speed = 0
        self.pos = Position(start_x, start_y, start_z, rot_x, rot_y, rot_z)
        self.rails = None
        self.train_next = None

        # Engine, passenger or freight
        self.type = type_train

    def create_object(self):
        model = Object3D(TRAINS_FOLDER, self.obj_name)

        if self.mtl_images:
            model.change_img(self.mtl_images, TRAINS_FOLDER)

        return model

    def generate(self):
        self.object.generate()

    def render(self):
        self.object.render(self.pos)

    def drive(self):
        if self.rails is None:
            return

        # TODO: change to begin-/endpoint
        if self.speed < 0 and afstand(*self.rails.ref_punt_next, *self.
                                      pos.get_x_y()) < abs(self.speed):
            if not self.rails.next:
                # End of rail, go in opposite direction.
                self.change_speed(self.speed)
            elif self.rails.type == RAILS_CURVE and \
                    self.rails.next.type == RAILS_CURVE and \
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
            elif self.rails.type == RAILS_CURVE and \
                    self.rails.prev.type == RAILS_CURVE and \
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
        if self.rails.type == RAILS_STRAIGHT:
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

        elif self.rails.type == RAILS_CURVE:
            rotation = self.pos.ry + SPEEDUP_CURVE * self.speed
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
        # if self.train_next:
        #     self.train_next.change_speed(-self.speed)

    def change_speed(self, speed):
        self.speed = -speed

    def attach_train(self, train=None):
        # Also possible to deattach train
        self.train_next = train

        # Change speed to own speed
        if train:
            self.train_next.change_speed(-self.speed)
