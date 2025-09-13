import pygame
import os

from rails import RailsType
from grid import Grid

pygame.init()
FONT = pygame.font.Font(None, 30)
COLOR_ACTIVE = (50, 120, 210)
COLOR_INACTIVE = (255, 255, 255)
COLOR_TEXT = (43, 56, 43)


class Commands:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.height = self.screen.get_size()[0]
        self.width = 23
        self.field = pygame.Rect(0, 0, self.height, self.width)
        self.command = ""
        self.active = False
        self.grid: Grid = None
        self.old_commands = []
        self.draw()

    def toggle(self):
        self.active = not self.active
        self.draw()

    def draw(self):
        self.field = pygame.Rect(0, 0, self.height, self.width)
        # pygame.draw.rect(self.screen, (0, 0, 0), self.field, width=1)
        color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        surface = pygame.Surface(self.field.size)
        surface.fill(color)
        self.screen.blit(surface, (0, 0))

    def typing(self, event):
        continue_game = True

        if event.key == pygame.K_RETURN:
            continue_game = self.run_command()
            self.command = ""
        elif event.key == pygame.K_BACKSPACE:
            self.command = self.command[:-1]
        else:
            self.command += event.unicode

        self.set_text()
        return continue_game

    def set_text(self, text=None):
        x, y = (0, 20)

        if not text:
            x, y = (1, 1)
            text = self.command

        pos = (self.field.x + x, self.field.y + y)
        # Remove current text
        # background = pygame.Surface((self.field.x + x, self.field.y + y))
        # self.screen.blit(background, pos)
        # pygame.draw.rect(self.screen, (0, 0, 0), self.field)
        self.draw()

        # Set new text
        text_surface = FONT.render(text, True, COLOR_TEXT)
        self.screen.blit(text_surface, pos)

    def run_command(self):
        command = self.command.split()
        output = "Unknown command"
        succes = False

        if command[0] == "add" and command[1] == "train":
            output, succes = self.add_train(command[2:])
        elif command == ["quit"]:
            pygame.quit()
            return False
        elif command[0] == "add" and command[1] in ["straight", "curve"]:
            text2type = {"straight": RailsType.STRAIGHT,
                         "curve": RailsType.CURVE}
            rails_type = text2type[command[1]]
            output, succes = self.add_rails(rails_type, command[2:])

        if succes:
            self.old_commands.append(self.command)

        print(output)
        # output write
        self.command = ""
        self.set_text()
        self.set_text(output)
        return True

    def add_train(self, args):
        try:
            x = int(args[0])
            y = int(args[1])
            angle = int(args[2])
            name = args[3]
            self.grid.add_train(x, y, angle, name)
            return "Added train", True
        except ValueError:
            return "The arguments of this command are invalid.", False
        except TypeError:
            return "Not the right type of the arguments.", False
        except FileNotFoundError:
            return "Train doesn't exists.", False
        except IndexError:
            return "Not the right amount of arguments.", False

    def add_rails(self, rails_type: RailsType, command):
        try:
            command = [int(c) for c in command]
            self.grid.add_rails(rails_type, *command)
            return "Added rail", True
        except ValueError:
            return "The arguments of this command are invalid.", False
        except TypeError:
            return "Not the right amount of arguments.", False
