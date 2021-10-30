import pygame
import math


pygame.init()
FONT = pygame.font.Font(None, 15)


class Rails:
    def __init__(self, grid, xh, yh, xv, yv):
        self.grid = grid
        self.xh = xh
        self.yh = yh
        self.xv = xv
        self.yv = yv
        self.middelpunt, self.straal_h, self.straal_v = self.middelpunten()

    def coord(self, x, y):
        return x, y

    def pythagoras(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2))

    def show_coordinate_system(self):
        step = 50

        for w in range(step, self.grid.get_size()[0], step):
            text_surface = FONT.render(str(w), True, (0, 0, 0))
            self.grid.blit(text_surface, (w, 2))

        for h in range(step, self.grid.get_size()[0], step):
            text_surface = FONT.render(str(h), True, (0, 0, 0))
            self.grid.blit(text_surface, (2, h))

    def draw(self):
        n = 10

        h_degrees = self.point_degree(self.xh, self.yh)
        v_degrees = self.point_degree(self.xv, self.yv)
        angle1, angle2 = self.get_start_stop_angles(h_degrees,
                                                    v_degrees)

        # self.draw_background(angle1, angle2, n)
        self.draw_omtrek_rails(angle1, angle2, n)
        self.draw_lines_between_rails(angle1, angle2, n)

    def middelpunten(self):
        middelpunt1 = (self.xh, self.yv)
        straal_x = abs(self.xh - self.xv)
        straal_y = abs(self.yh - self.yv)

        return middelpunt1, straal_x, straal_y

    def get_start_stop_angles(self, h_degrees, v_degrees):
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

    def draw_omtrek_rails(self, start_angle, stop_angle, n):
        for i in [n, -n]:
            rect = [self.middelpunt[0] - self.straal_h - i,
                    self.middelpunt[1] - self.straal_v - i,
                    2 * self.straal_h + 2 * i,
                    2 * self.straal_v + 2 * i]

            pygame.draw.arc(self.grid, (0, 0, 0), rect,
                            math.radians(start_angle),
                            math.radians(stop_angle))

    def draw_lines_between_rails(self, start_angle, stop_angle, n):
        mid_x, mid_y = self.middelpunt
        alpha = 90 / 4

        if start_angle > stop_angle:
            stop_angle += 360

        degree = start_angle
        x1 = mid_x + (self.straal_h + n) * math.cos(math.radians(degree))
        y1 = mid_y - (self.straal_v + n) * math.sin(math.radians(degree))
        x2 = mid_x + (self.straal_h - n) * math.cos(math.radians(degree))
        y2 = mid_y - (self.straal_v - n) * math.sin(math.radians(degree))

        while degree <= stop_angle:
            pygame.draw.line(self.grid, (130, 130, 130), (x1, y1), (x2, y2))

            degree += alpha
            x1 = mid_x + (self.straal_h + n) * math.cos(math.radians(degree))
            y1 = mid_y - (self.straal_v + n) * math.sin(math.radians(degree))
            x2 = mid_x + (self.straal_h - n) * math.cos(math.radians(degree))
            y2 = mid_y - (self.straal_v - n) * math.sin(math.radians(degree))

    def draw_background(self, start_angle, stop_angle, n):
          # draw background
        if start_angle > stop_angle:
            stop_angle += 360

        rect = [self.middelpunt[0] - self.straal_h - n,
                self.middelpunt[1] - self.straal_v - n,
                2 * self.straal_h + 2 * n,
                2 * self.straal_v + 2 * n]
        pygame.draw.arc(self.grid, (200, 200, 200), rect, start_angle, stop_angle, width=2 * n)


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
    # points = [((100, 110), (120, 60)),
    #           ((100, 10), (120, 60)),
    #           ((100, 10), (80, 60)),
    #           ((100, 110), (80, 60))]
    # points = [((100, 10), (120, 60))]
    # points = [((100, 10), (80, 60))]
    # points = [((50, 50), (80, 30))]
    # points = [((50, 50), (20, 30))]
    # points = [((50, 10), (80, 30))]
    loop = True
    rs = []
    clock = pygame.time.Clock()
    # colors = [(0, 0, 0), (250, 0, 0), (0, 250, 0), (0, 0, 250), (125, 0, 0),
    #           (0, 125, 0), (0, 0, 125)]

    for p1, p2 in points:
        r = Rails(screen, *p1, *p2)
        r.middelpunten()
        rs.append(r)

    r.show_coordinate_system()

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False

        [r.draw() for r in rs]
        pygame.display.flip()
        # pygame.display.update()
        clock.tick(60)

    pygame.quit()
