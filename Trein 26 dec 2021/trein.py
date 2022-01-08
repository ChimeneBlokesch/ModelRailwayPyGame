import math
from objparser import Object3D

from constants import Punt, TREINEN_MAP, angle_between
from rails import RAILS_BOCHT, RAILS_RECHT


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
        # return self.pos.x, self.pos.y
        return self.ref_punt

    def rijden(self):
        if self.rails.ref_punt_next == self.ref_punt:
            print("Next rails")
            self.rails = self.rails.next

        # iets met rails waardoor de nieuwe positie en rotatie bepaald
        # kan worden.
        # rails.angle en rails.rotation

        # Afhankelijk van rails.angle maakt de trein een rotatie
        if self.rails.type == RAILS_RECHT:
            # 0 of 180
            self.rotate(x=self.rails.rotation-self.start_angle)
            old_x, old_y = self.ref_punt
            TEMP_SCALE = 100
            old_x *= TEMP_SCALE
            old_y *= TEMP_SCALE

            if self.rails.rotation == 0:
                # Horizontaal
                self.move(x=self.speed + self.pos.x)
                self.ref_punt = ((old_x + self.speed * TEMP_SCALE) / TEMP_SCALE,
                                 old_y / TEMP_SCALE)
            elif self.rails.rotation == 90:
                # Verticaal
                self.move(y=self.speed + self.pos.y)
                self.ref_punt = (round(old_x / TEMP_SCALE, 2),
                                 round((old_y + self.speed * TEMP_SCALE) /
                                 TEMP_SCALE, 2))
            else:
                print(self.rails.rotation, "== -90?")
        elif self.rails.type == RAILS_BOCHT:
            # 90
            # eenheidscirkel
            # hoek tussen self.pos en rails.ref_punt_prev
            angle = angle_between(self.ref_punt,
                                  self.rails.ref_punt_prev)
            print("rotation voor", self.rotate_pos.x)
            rotation = angle+self.rails.rotation-self.start_angle

            # Om vooruit te komen, wordt de rotation verhoogd.
            rotation += self.speed
            self.rotate(y=rotation)  # y is het zeker
            print("rotation na", rotation)
            print("angle between ref punt", self.ref_punt, "and prev ref punt",
                  self.rails.ref_punt_prev, "is", angle)
            # Er moet misschien rekening met het min teken gehouden worden.
            width = abs(
                self.rails.ref_punt_prev[0] - self.rails.ref_punt_next[0])
            height = abs(
                self.rails.ref_punt_prev[1] - self.rails.ref_punt_next[1])

            if self.rails.rotation in [90, 135, 180, 225]:
                if max(self.rails.ref_punt_prev[1], self.rails.ref_punt_next[1]
                       ) == self.rails.ref_punt_next:
                    pos_x = self.rails.ref_punt_next[0]
                    pos_y = self.rails.ref_punt_prev[1]
                else:
                    pos_x = self.rails.ref_punt_next[1]
                    pos_y = self.rails.ref_punt_prev[0]
            else:
                if min(self.rails.ref_punt_prev[1], self.rails.ref_punt_next[1]
                       ) == self.rails.ref_punt_next:
                    pos_x = self.rails.ref_punt_next[0]
                    pos_y = self.rails.ref_punt_prev[1]
                else:
                    pos_x = self.rails.ref_punt_next[1]
                    pos_y = self.rails.ref_punt_prev[0]

            # pos_x = max(
            #     self.rails.ref_punt_prev[0], self.rails.ref_punt_next[0])
            # pos_y = max(
            #     self.rails.ref_punt_prev[1], self.rails.ref_punt_next[1])

            # iets met angle doen om nieuwe positie te berekenen
            self.ref_punt = (round(width * math.cos(rotation) + pos_x, 2),
                             round(height * math.sin(rotation) + pos_y, 2))
            # self.ref_punt = (round(self.speed * math.cos(rotation), 2),
            #                  round(self.speed * math.sin(rotation), 2))
            # self.ref_punt = (round(math.cos(rotation) + self.speed, 2),
            #                  round(math.sin(rotation) + self.speed, 2))
            # print("new ref punt", self.ref_punt)

            angle = angle_between((self.pos[0], self.pos[1]),
                                  self.rails.ref_punt_prev)
            rotation = angle+self.rails.rotation-self.start_angle

            # Om vooruit te komen, wordt de rotation verhoogd.
            rotation += self.speed

            self.move(x=round(width * math.cos(rotation) + pos_x, 2),
                      y=round(height * math.sin(rotation) + pos_y, 2))

            # self.move(x=self.speed + self.pos.x,
            #           y=self.speed + self.pos.y)
            print("new2 ref punt", self.ref_punt)
            print("new pos", self.pos)
            print()

    def change_speed(self, speed):
        self.speed = speed
