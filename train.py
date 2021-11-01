import pygame

HEIGHT = 100

LENGTH = 20


class Train:
    def __init__(self, grid, start_x: int, start_y: int,
                 angle: int, filename: str):
        self.grid = grid
        self.x = start_x
        self.y = start_y
        self.angle = angle
        self.speed = 0
        self.max_speed = 10
        self.filename = filename
        self.properties = self.grid.treinen_db.get_trein(filename)
        self.trein_ervoor = None
        self.trein_erachter = None

    def draw(self):
        # pygame.draw.rect(self.screen, self.color, (self.x, self.y, -40, -10),
        #                  width=10)
        try:
            train = pygame.image.load(self.filename)
        except FileNotFoundError:
            return

        size = train.get_size()
        width = size[1] * HEIGHT / size[0]
        train = pygame.transform.smoothscale(train, (HEIGHT, width))
        train = pygame.transform.rotate(train, self.angle)
        self.grid.grid.blit(train, (self.x, self.y - 0.5 * width))

    def koppel_voor(self, trein_ervoor):
        self.trein_ervoor = trein_ervoor

    def ontkoppel_voor(self):
        self.trein_ervoor = None

    def koppel_achter(self, trein_erachter):
        self.trein_erachter = trein_erachter

    def ontkoppel_achter(self):
        self.trein_erachter = None
