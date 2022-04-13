import numpy as np


class Position:
    def __init__(self, x=0, y=0, z=0, rx=0, ry=0, rz=0):  # tilt=0, pan=0):
        """
        tilt: vertical rotation
        pan: horizontal rotation
        """
        self.x = x
        self.y = y
        self.z = z
        # self.tilt = tilt  # Vertical rotation
        # self.pan = pan  # Horizontal rotation
        self.rx = rx
        self.ry = ry
        self.rz = rz

    def move(self, x=None, y=None, z=None):
        if x:
            self.x = x

        if y:
            self.y = y

        if z:
            self.z = z

    # def rotate(self, tilt=None, pan=None):
    #     """
    #     tilt: vertical rotation
    #     pan: horizontal rotation
    #     """
    #     if tilt:
    #         self.tilt = tilt % 360

    #     if pan:
    #         self.pan = pan % 360

    def rotate(self, x=None, y=None, z=None):
        if x:
            self.rx = x % 360

        if y:
            self.ry = y % 360

        if z:
            self.rz = z % 360

    def move_delta(self, dx=0, dy=0, dz=0):
        self.move(self.x + dx, self.y + dy, self.z + dz)

    # def rotate_delta(self, d_tilt=0, d_pan=0):
    #     """
    #     tilt: vertical rotation
    #     pan: horizontal rotation
    #     """
    #     self.rotate(self.tilt + d_tilt,
    #                 self.pan + d_pan)

    def rotate_delta(self, dx=0, dy=0, dz=0):
        self.rotate(self.rx + dx, self.ry+dy, self.rz+dz)

    def get_x_y(self):
        return self.x, self.y

    def get_pos(self):
        return self.x, self.y, self.z

    def get_rotate(self):
        return self.rx, self.ry, self.rz

    def is_equal(self, pos2):
        return np.allclose(self.get_pos(), pos2.get_pos()) and \
            np.allclose(self.get_rotate(), pos2.get_rotate())
