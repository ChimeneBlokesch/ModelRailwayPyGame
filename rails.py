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
        rect = pygame.Rect(*self.middelpunt,
                           4 * self.straal_v, 4 * self.straal_h)
        rect = [*self.middelpunt, 4 * self.straal_v, 4 * self.straal_h]
        start_angle, stop_angle = self.start_stop_degrees()
        a = pygame.draw.arc(self.grid, c, rect,
                            math.radians(start_angle),
                            math.radians(stop_angle))
        # print(rect.x, rect.y, rect.width, rect.height)
        print(a)
        # print(self.hoek("l", "u"), self.coord(*self.hoek("l", "u")))

    def middelpunten(self):
        middelpunt1 = (self.xh, self.yv)
        straal_x = abs(self.xh - self.xv)
        straal_y = abs(self.yh - self.yv)

        return middelpunt1, straal_x, straal_y

    def start_stop_degrees(self):
        h_degrees = self.point_degree(self.xh, self.yh)
        v_degrees = self.point_degree(self.xv, self.yv)
        print("h_degrees", h_degrees)
        print("v_degrees", v_degrees)
        start_angle = h_degrees
        stop_angle = v_degrees
        print("start_angle", start_angle)
        print("stop_angle", stop_angle)

        # if start_angle > stop_angle:
        #     start_angle, stop_angle = stop_angle, abs(stop_angle - start_angle)

        # right - 90 = top
        # start_angle = 0
        # stop_angle = 90

        # right - 180 = left
        # start_angle = 0
        # stop_angle = 180

        # right - 270 = down
        # start_angle = 0
        # stop_angle = 270

        # if start_angle > stop_angle met klok
        # if stop_angle > start_angle tegen klok

        # 180 left + 270 = down (met klok)
        # start_angle = 270
        # stop_angle = 180

        # # 180 left + 270 = down (tegen klok)
        # start_angle = 270
        # stop_angle = 180
        # start_angle, stop_angle = stop_angle, start_angle

        # a = 270
        # b = 180

        # 180 left -> 90 down start_angle > stop_angle (met klok)
        # start_angle = min(a, b)
        # stop_angle = max(a, b) - start_angle

        # start_angle > stop_angle
        # stop_angle + (start_angle % 360) = stop
        # start = stop_angle

        # 270 > 180
        # 180 + (450 % 360) = 180 + 90
        # start_angle = min(a, b) + max(a, b)  # 180 + 270 = 450
        # stop_angle = min(a, b)

        if h_degrees == v_degrees:
            return h_degrees, v_degrees

        # if h_degrees > v_degrees:
        #     start_angle = max(h_degrees, v_degrees) - min(h_degrees, v_degrees)
        #     stop_angle = min(h_degrees, v_degrees)
        # else:
        #     start_angle = max(h_degrees, v_degrees)
        #     stop_angle = min(h_degrees, v_degrees) + max(h_degrees, v_degrees)

        # voor 0   -> 90  start = 270 end = 0       start = 360 - max   end = min
        # voor 180 -> 270 start = 90  end = 180     start = 360 - max   end = min
        # voor 270 -> 0   start = 0   end = 90      start = min         end = 360 - max
        # voor 90 -> 180  start = 180 end = 270     start = max         end = 360 - min
        # start_angle = 360 - max(h_degrees, v_degrees)  # 360 - max
        # stop_angle = min(h_degrees, v_degrees)  # min

        # start_angle = 180
        # stop_angle = 270
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




        # if a > b:
        #     start_angle = min(a, b) + max(a, b)  # 180 + 270 = 450
        #     stop_angle = min(a, b)
        # elif a < b:
        #     start_angle = min(a, b)
        #     stop_angle = min(a, b) + max(a, b)



        # top + ? = left (tegen klok) dus stop_angle > start_angle

        # start_angle, stop_angle = max(start_angle, stop_angle), stop_angle
        # start_angle -= 360

        print("start_angle", start_angle)
        print("stop_angle", stop_angle)
        # is_left = self.xv == self.middelpunt[0] - self.straal_h
        # is_right = self.xv == self.middelpunt[0] + self.straal_h
        # stop_angle_left = 90 * (2 * ((is_left) | 0) + 1)
        # stop_angle_right = 90 * (2 * ((is_right) | 0) - 1)
        # print("middelpunt", self.middelpunt)
        # print("start_angle", start_angle)
        # print("stop_angle left", stop_angle_left)
        # print("stop_angle right", stop_angle_right)
        return start_angle, stop_angle
        # waar -> 3
        # niet waar -> 1

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

    def richting(self, x, y):
        """
        Geeft aan of (x, y) boven, beneden, links of rechts is tov.
        het middelpunt.
        """
        if x == self.middelpunt[0]:
            if y == self.middelpunt[1] - self.straal_h:
                # top
                return "t"
            if y == self.middelpunt[1] - self.straal_v:
                # bottom
                return "b"

        if y == self.middelpunt[1]:
            if x == self.middelpunt[0] - self.straal_h:
                # left
                return "l"
            if x == self.middelpunt[0] + self.straal_h:
                # right
                return "r"

    def hoek(self, lr, ud):
        x = self.middelpunt[0]
        y = self.middelpunt[1]

        if lr.start_angleswith("l"):
            x -= self.straal
        else:
            x += self.straal

        if ud.start_angleswith("u"):
            y -= self.straal
        else:
            y += self.straal

        # y = self.middelpunt[1] + -1 * i + 1 * ((ud == "u") | 0)

        return x, y


# Only used for testing:
if __name__ == "__main__":
    screen = pygame.display.set_mode([1000, 600])
    pygame.display.set_caption("Rails")
    screen.fill((255, 255, 255))
    # straal_h = 30
    # straal_v = 20
    #  h = (50, 50), v = (80, 30) middelpunt = (50, 30)
    #  h = (80, 30), v = (50, 50) middelpunt = (80, 50)

    # straal_h = 20
    # straal_v = 50
    #  h = (80, 60), v = (100, 10) middelpunt = (80, 10)
    #  h = (100, 10), v = (80, 60) middelpunt = (100, 60)

    # h = (a, b),   v = (c, d) middelpunt = (a, d)
    points = [((50, 50), (80, 30)), ((80, 30), (50, 50)), ((50, 10), (20, 30)),
              ((100, 10), (80, 60)), ((80, 60), (100, 10)), ((100, 10), (120, 60))]
    # points = [((100, 10), (120, 60))]
    # points = [((100, 10), (80, 60))]
    # points = [((50, 50), (80, 30))]
    loop = True
    rs = []
    clock = pygame.time.Clock()
    colors = [(0, 0, 0), (250, 0, 0), (0, 250, 0), (0, 0, 250), (125, 0, 0), (0, 125, 0), (0, 0, 125)]

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

    # start_angle angle 0, stop_angle angle 90
