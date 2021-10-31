import math
import pygame


class Recht:
    def __init__(self, x1, y1, x2, y2):
        self.n = 10
        self.x1, self.y1, self.x2, self.y2 = self.sort_points(x1, y1, x2, y2)
        print("1", (self.x1, self.y1))
        print("2", (self.x2, self.y2))
        # self.x, self.y = self.position()
        # print("position", (self.x, self.y))
        # self.surface = pygame.Surface()

    def sort_points(self, x1, y1, x2, y2):
        if x1 < x2 or (x1 == x2 and y1 < y2):
            return x1, y1, x2, y2

        return x2, y2, x1, y1

    def position(self):
        min_x = self.x1
        min_y = min(self.y1, self.y2)
        pos = (min_x - self.n, min_y - self.n)
        ...

    def dist(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def calculate(self):
        ...

    def calculate2(self):
        a = (self.x1, self.y1)
        b = (self.x2, self.y2)
        c = (max(self.x1, self.y1), max(self.x2, self.y2))
        d = (self.x, self.y)

        if a == c and b == d:
            c = (min(self.x1, self.x2), max(self.y1, self.y2))
            d = (max(self.x1, self.x2), max(self.y1, self.y2))

        ab = self.dist(*a, *b)
        bc = self.dist(*b, *c)
        alpha = math.asin(bc / ab)
        ae = self.n
        # cos(alpha) = af / ae
        # sin(alpha) = af / ef
        # 1 / sin(alpha) = ef / af
        # af / sin(alpha) = ef
        af = math.cos(alpha) * ae
        ef = af / math.cos(alpha)
        # sin(alpha) = ag / ae
        ag = math.sin(alpha) * ae

    def draw(self):
        ...


# Only for testing
if __name__ == "__main__":
    r1 = Recht(1, 9, 4, 1)
    r2 = Recht(1, 1, 4, 9)
    r3 = Recht(4, 1, 1, 9)
    r4 = Recht(4, 9, 1, 1)
    # r3 = Recht(3, 2, 7, 8)
