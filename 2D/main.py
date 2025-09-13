# Inspiration for this code:
# https://medium.com/@plaha.roshan/creating-a-simple-train-simulator-with-pygame-182204df7f04

import pygame
import os

from commands import Commands
from grid import Grid
from database_trains import Database
from rails import RailsType

if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()

    flags = 0

    screen = pygame.display.set_mode([1000, 600], flags)
    pygame.display.set_caption("Model Railway 2D")
    screen.fill((255, 255, 255))

    loop = True
    command_field = Commands(screen)
    command_field.draw()
    trains_db = Database()
    grid = Grid(screen, (0, command_field.field.size[1]), trains_db)

    # Initialize the grid with a train on an oval rails
    grid.add_train(250, 50, 0,
                   os.path.join("sprites", "trains", "custom_side.png"))
    grid.add_rails(RailsType.CURVE, 150, 50, 100, 100)
    grid.add_rails(RailsType.STRAIGHT, 150, 50, 750, 50)
    grid.add_rails(RailsType.CURVE, 150, 150, 100, 100)
    grid.add_rails(RailsType.STRAIGHT, 150, 150, 750, 150)
    grid.add_rails(RailsType.CURVE, 750, 50, 800, 100)
    grid.add_rails(RailsType.CURVE, 750, 150, 800, 100)

    command_field.grid = grid

    # Keeps the game running
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False

            # Detect whether the command-line should be active or not
            if event.type == pygame.MOUSEBUTTONDOWN:
                if command_field.field.collidepoint(event.pos):
                    command_field.toggle()
                else:
                    command_field.active = False

            if event.type == pygame.KEYDOWN:
                # Use the input character for the command
                if command_field.active:
                    loop = command_field.typing(event)

        command_field.set_text()

        # pygame.display.update()
        pygame.display.flip()

        grid.draw()
        clock.tick(60)

pygame.quit()
