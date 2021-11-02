# https://medium.com/@plaha.roshan/creating-a-simple-train-simulator-with-pygame-182204df7f04

import pygame
from commands import Commands
from game_grid import Grid
from database_treinen import Treinen


if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    # flags = pygame.FULLSCREEN | pygame.RESIZABLE
    flags = 0
    screen = pygame.display.set_mode([1000, 600], flags)
    pygame.display.set_caption("Treinen")
    screen.fill((255, 255, 255))
    # background = pygame.Surface(screen.get_size())
    loop = True
    command_field = Commands(screen)
    command_field.draw()
    treinen_db = Treinen()
    grid = Grid(screen, (0, command_field.field.size[1]), treinen_db)
    grid.add_train(250, 50, 0, "Treinen/VIRM_kop_links.png")
    grid.add_rails(0, 150, 50, 100, 100)
    grid.add_rails(1, 150, 50, 750, 50)
    grid.add_rails(0, 150, 150, 100, 100)
    grid.add_rails(1, 150, 150, 750, 150)
    grid.add_rails(0, 750, 50, 800, 100)
    grid.add_rails(0, 750, 150, 800, 100)

    command_field.grid = grid

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if command_field.field.collidepoint(event.pos):
                    command_field.toggle()
                else:
                    command_field.active = False

            if event.type == pygame.KEYDOWN:
                if command_field.active:
                    loop = command_field.typing(event)

        command_field.set_text()

        # pygame.display.update()
        pygame.display.flip()

        grid.draw()
        clock.tick(60)

pygame.quit()
