import math
import pygame


class Recht:
    def __init__(self, x1, y1, x2, y2):
        self.n = 10
        self.x1, self.y1, self.x2, self.y2 = self.sort_points(x1, y1, x2, y2)
        self.vector_line, self.points = self.get_vector_n()
        print("vector", self.vector_line)
        [print("point", x) for x in self.points]
        # print("1", (self.x1, self.y1))
        # print("2", (self.x2, self.y2))
        # self.x, self.y = self.position()
        # print("position", (self.x, self.y))
        points_x = [x for x, _ in self.points]
        points_y = [y for _, y in self.points]
        self.x = min(points_x)
        self.y = min(points_y)
        max_x = max(points_x)
        max_y = max(points_y)
        width = max_x - self.x
        height = max_y - self.y
        self.surface = pygame.Surface((width, height))
        self.surface.fill((255, 0, 255))

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

    def length_vector(self, x, y):
        return math.sqrt(x ** 2 + y ** 2)

    def get_vector_n(self):  # line_points
        points = []
        line = (self.x2 - self.x1, self.y2 - self.y1)
        print("l", line)
        lengte_lijn = self.length_vector(*line)
        vector_l = tuple(x / lengte_lijn for x in line)
        n = (self.n * -vector_l[1], self.n * vector_l[0])
        points.append((self.x1 + n[0], self.y1 + n[1]))
        points.append((self.x2 + n[0], self.y2 + n[1]))
        points.append((self.x1 - n[0], self.y1 - n[1]))
        points.append((self.x2 - n[0], self.y2 - n[1]))

        # Dit misschien voor andere lijnen
        # n = (l[1], l[0])
        # n = tuple(a * x for x in n)
        # points.append((self.x1 + n[0], self.y1 + n[1]))
        # points.append((self.x1 - n[0], self.y1 - n[1]))
        # [print(p) for p in points]
        return vector_l, points







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

    def point(self, p):
        return p[0] - self.x, p[1] - self.y

    def draw(self):
        pygame.draw.line(self.surface, (0, 0, 0),
                         self.point((self.x1, self.y1)),
                         self.point((self.x2, self.y2)))
        x1, y1 = self.point(self.points[0])
        x2, y2 = self.point(self.points[1])
        x3, y3 = self.point(self.points[2])
        x4, y4 = self.point(self.points[3])
        pygame.draw.line(self.surface, (0, 0, 255), (x1, y1), (x2, y2))
        pygame.draw.line(self.surface, (0, 0, 255), (x3, y3), (x4, y4))
        # print("dist", self.dist(x1, y1, x2, y2))
        vector_line = (self.x2 - self.x1, self.y2 - self.y1)
        length_line = self.dist(x1, y1, x2, y2)
        vector_line = (vector_line[0] / length_line,
                       vector_line[1] / length_line)

        for i in range(0, math.floor(length_line), 15):
            vector = tuple(x * i for x in vector_line)
            # print("vector", vector)
            # print((x1 + vector[0], y1 - vector[1]))
            # print((x3 + vector[0], y3 - vector[1]))
            # exit()
            pygame.draw.line(self.surface, (0, 0, 255),
                             (x1 + vector[0], y1 + vector[1]),
                             (x3 + vector[0], y3 + vector[1]))

        pygame.draw.line(self.surface, (0, 0, 255), (x2, y2), (x4, y4))

        # pygame.draw.line(self.surface, (0, 0, 255), (x1, y1), (x3, y3))
        # pygame.draw.line(self.surface, (0, 0, 255), (x2, y2), (x4, y4))


# Only for testing
if __name__ == "__main__":
    r1 = Recht(10, 90, 40, 10)
    r2 = Recht(10, 10, 40, 90)
    r3 = Recht(40, 10, 10, 90)
    r4 = Recht(40, 90, 10, 10)
    r5 = Recht(30, 20, 70, 80)
    r = [r1]
    loop = True

    screen = pygame.display.set_mode([1000, 600])
    pygame.display.set_caption("Rails")
    screen.fill((255, 255, 255))

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False

        for x in r:
            x.draw()
            screen.blit(x.surface, (x.x, x.y))

        pygame.display.flip()

    pygame.quit()
