from objparser import Object3D

from constants import Punt, TREINEN_MAP, angle_between
from rails import RAILS_BOCHT, RAILS_RECHT


class Trein:
    def __init__(self, name, filename, x, y):
        self.name = name
        self.path_to_obj_file = TREINEN_MAP + filename
        self.object = self.create_object()
        self.start_angle = 0
        self.speed = (0, 0)
        self.rotate_pos = Punt(0, 0, 0)
        self.pos = Punt(0, 0, 0)

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
        return self.pos.x, self.pos.y

    def rijden(self, rails=None):
        if rails is not None:
            self.rails = rails
        # iets met rails waardoor de nieuwe positie en rotatie bepaald
        # kan worden.
        # rails.angle en rails.rotation

        # Afhankelijk van rails.angle maakt de trein een rotatie
        if rails.type == RAILS_RECHT:
            # 0 of 180
            self.rotate(x=rails.rotation-self.start_angle)

            if rails.rotation == 0:
                self.move(x=self.speed[0] + self.pos.x)
            elif rails.rotation == 180:
                self.move(y=self.speed[0] + self.pos.y)
            else:
                print(rails.rotation, "== -180?")
        elif rails.type == RAILS_BOCHT:
            # 90
            # eenheidscirkel
            # hoek tussen self.pos en rails.ref_punt_prev
            angle = angle_between((self.pos.x, self.pos.y),
                                  rails.ref_punt_prev)
            self.rotate(x=angle+rails.rotation-self.start_angle)
            # Er moet misschien rekening met het min teken gehouden worden.
            self.move(x=self.speed[0] + self.pos.x,
                      y=self.speed[1] + self.pos.y)

    def change_speed(self, speed):
        self.speed = speed
