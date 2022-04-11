class Position:
    def __init__(self, x=0, y=0, z=0, tilt=0, pan=0):
        self.x = x
        self.y = y
        self.z = z
        self.tilt = tilt  # Vertical rotation
        self.pan = pan  # Horizontal rotation

    def move(self, x=None, y=None, z=None):
        if x:
            self.x = x

        if y:
            self.y = y

        if z:
            self.z = z

    def rotate(self, tilt=None, pan=None):
        if tilt:
            self.tilt = tilt % 360

        if pan:
            self.pan = pan % 360

    def move_delta(self, dx=0, dy=0, dz=0):
        self.move(self.x + dx, self.y + dy, self.z + dz)

    def rotate_delta(self, d_tilt=0, d_pan=0):
        self.rotate(self.tilt + d_tilt,
                    self.pan + d_pan)
