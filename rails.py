import pygame
import math


class Rails:
    def __init__(self, grid, xh, yh, xv, yv):
        self.grid = grid
        self.xh = xh
        self.yh = yh
        self.xv = xv
        self.yv = yv
        self.middelpunt, self.straal_h, self.straal_v = self.middelpunten()
        print("middelpunt", self.middelpunt)
        print("straal_h", self.straal_h)
        print("straal_v", self.straal_v)

    def coord(self, x, y):
        return x, y

    def draw(self, c):
        rect = [*self.middelpunt, 4 * self.straal_h, 4 * self.straal_v]
        start_angle, stop_angle = self.start_stop_degrees()
        pygame.draw.arc(self.grid, c, rect,
                        math.radians(start_angle),
                        math.radians(stop_angle))

    def middelpunten(self):
        middelpunt1 = (self.xh, self.yv)
        straal_x = abs(self.xh - self.xv)
        straal_y = abs(self.yh - self.yv)

        return middelpunt1, straal_x, straal_y

    def start_stop_degrees(self):
        h_degrees = self.point_degree(self.xh, self.yh)
        v_degrees = self.point_degree(self.xv, self.yv)

        if h_degrees == v_degrees:
            return h_degrees, v_degrees

        degrees = [h_degrees, v_degrees]

        if 0 in degrees and 90 in degrees:
            start_angle = 270
            stop_angle = 0
        elif 90 in degrees and 180 in degrees:
            start_angle = 180
            stop_angle = 270
        elif 180 in degrees and 270 in degrees:
            start_angle = 90
            stop_angle = 180
        elif 270 in degrees and 0 in degrees:
            start_angle = 0
            stop_angle = 90
        else:
            return h_degrees, v_degrees

        return start_angle, stop_angle

    def point_degree(self, x, y):
        if y == self.middelpunt[1] + self.straal_v:
            # bottom
            return 90
        elif y == self.middelpunt[1] - self.straal_v:
            # top
            return 270
        elif x == self.middelpunt[0] - self.straal_h:
            # left
            return 180

        # right
        return 0


# Only used for testing:
if __name__ == "__main__":
    screen = pygame.display.set_mode([1000, 600])
    pygame.display.set_caption("Rails")
    screen.fill((255, 255, 255))

    points = [((50, 50), (80, 30)), ((80, 30), (50, 50)),
              ((50, 10), (20, 30)),
              ((100, 10), (80, 60)), ((80, 60), (100, 10)),
              ((100, 10), (120, 60))]
    points = [((50, 50), (80, 30)),
              ((50, 10), (80, 30)),
              ((50, 10), (20, 30)),
              ((50, 50), (20, 30))]
    points = [((100, 110), (120, 60)),
              ((100, 10), (120, 60)),
              ((100, 10), (80, 60)),
              ((100, 110), (80, 60))]
    # points = [((100, 10), (120, 60))]
    # points = [((100, 10), (80, 60))]
    # points = [((50, 50), (80, 30))]
    loop = True
    rs = []
    clock = pygame.time.Clock()
    colors = [(0, 0, 0), (250, 0, 0), (0, 250, 0), (0, 0, 250), (125, 0, 0),
              (0, 125, 0), (0, 0, 125)]

    for p1, p2 in points:
        r = Rails(screen, *p1, *p2)
        r.middelpunten()
        rs.append(r)

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False

        [r.draw(colors[i]) for i, r in enumerate(rs)]
        pygame.display.flip()
        # pygame.display.update()
        clock.tick(60)

    pygame.quit()
