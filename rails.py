import pygame

from bocht import Bocht


pygame.init()
FONT = pygame.font.Font(None, 15)


class Rails:
    def __init__(self, grid, x1, y1, x2, y2):
        self.grid = grid
        self.rails = self.new_rails(x1, y1, x2, y2)

    def new_rails(self, x1, y1, x2, y2):
        if x1 == x2:
            return

        if y1 == y2:
            return

        return Bocht(x1, y1, x2, y2)

    def draw(self):
        self.rails.draw()
        self.grid.blit(self.rails.surface, (self.rails.x, self.rails.y))


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
    points = [((50, 10), (80, 30))]
    loop = True
    rs = []
    clock = pygame.time.Clock()
    # colors = [(0, 0, 0), (250, 0, 0), (0, 250, 0), (0, 0, 250), (125, 0, 0),
    #           (0, 125, 0), (0, 0, 125)]

    for p1, p2 in points:
        r = Rails(screen, *p1, *p2)
        rs.append(r)

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False

        [r.draw() for r in rs]
        pygame.display.flip()
        # pygame.display.update()
        clock.tick(60)

    pygame.quit()
