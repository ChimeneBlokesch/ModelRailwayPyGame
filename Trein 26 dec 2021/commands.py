import pygame
from constants import TREINEN_MAP
from grid import Grid
from rails import RAILS_RECHT, RAILS_BOCHT

pygame.init()
FONT = pygame.font.Font(None, 30)
COLOR_ACTIVE = (50, 120, 210)
COLOR_INACTIVE = (255, 255, 255)
COLOR_TEXT = (43, 56, 43)


class Commands:
    def __init__(self, screen: pygame.Surface, grid: Grid):
        self.screen = screen
        self.height = self.screen.get_size()[0]
        self.width = 23
        self.field = pygame.Rect(0, 0, self.height, self.width)
        self.command = ""
        self.active = False
        self.grid = grid
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
            output, succes = self.add_trein(command[2:])
        elif command == ["quit"]:
            pygame.quit()
            return False
        elif command[0] == "add" and command[1] in ["recht", "bocht"]:
            output, succes = self.add_rails(command[1], command[2:])

        if succes:
            self.old_commands.append(self.command)

        print(output)
        # output write
        self.command = ""
        self.set_text()
        self.set_text(output)
        return True

    def add_trein(self, args):
        try:
            name = args[0]
            filename = TREINEN_MAP + args[1] + ".obj"
            self.grid.add_trein(name, filename)
            return "Added train", True
        except ValueError:
            return "The arguments of this command are invalid.", False
        except TypeError:
            return "Not the right type of the arguments.", False
        except FileNotFoundError:
            return "Train doesn't exists.", False
        except IndexError:
            return "Not the right amount of arguments.", False

    def add_rails(self, type_rails, command):
        if type_rails == "recht":
            type_rails = RAILS_RECHT
        elif type_rails == "bocht":
            type_rails = RAILS_BOCHT
        else:
            return

        angle = 0
        is_flipped = False
        pos_x, pos_y, pos_z = (0, 0, 0)
        rotation = 0

        try:
            command = command.split("=")

            for i in range(0, len(command), 2):
                if command[i] == "angle":
                    angle = float(command[i+1])
                elif command[i] == "is_flipped":
                    is_flipped = command[i+1] == "True"
                elif command[i] == "pos_x":
                    pos_x = float(command[i+1])
                elif command[i] == "pos_y":
                    pos_y = float(command[i+1])
                elif command[i] == "pos_z":
                    pos_z = float(command[i+1])
                elif command[i] == "rotation":
                    rotation = float(command[i+1])
            self.grid.add_rails(type_rails, angle=angle, is_flipped=is_flipped,
                                pos_x=pos_x, pos_y=pos_y, pos_z=pos_z,
                                rotation=rotation)
            return "Added rail", True
        except ValueError:
            return "The arguments of this command are invalid.", False
        except TypeError:
            return "Not the right amount of arguments.", False
