import sys
import numpy as np
import pygame
import OpenGL.GL as GL
import OpenGL.GLU as GLU
from camera import CAMERA_FREE, CAMERA_POPPETJE, Camera
from constants import angle_between_vectors, print_rails_info, show_coordinates
from grid import Grid
from lijnen import create_line
from trein import TREIN_LOCOMOTIEF, TREIN_PASSAGIER
import math

MOVE_STEP = 0.05
ROTATE_STEP = 1


class Game:
    def __init__(self):
        pygame.init()

        viewport = (800, 600)
        # hx = viewport[0]/2
        # hy = viewport[1]/2
        self.srf = pygame.display.set_mode(viewport,
                                           pygame.OPENGL | pygame.DOUBLEBUF)

        GL.glEnable(GL.GL_COLOR_MATERIAL)
        GL.glEnable(GL.GL_DEPTH_TEST)
        # most obj files expect to be smooth-shaded
        GL.glShadeModel(GL.GL_SMOOTH)

        self.grid = Grid()
        self.camera = Camera()

        self.peper = self.grid.add_poppetje("Pepper", "lego_pepper2",
                                            rot_x=90, rot_y=180)

        self.grid.generate()

        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        width, height = viewport
        GLU.gluPerspective(90.0, width/float(height), 1, 100.0)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glMatrixMode(GL.GL_MODELVIEW)

        # This is needed for transparency.
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

    def loop(self):
        pygame.event.pump()

        self.handle_events()

        keys = pygame.key.get_pressed()
        diff_pos, diff_rotate_pos = self.camera.render(keys)
        # print("HIER", diff_pos, diff_rotate_pos, self.camera.mode)

        tx, ty, tz = self.camera.pos
        rx, ry, rz = self.camera.rotate_pos

        # Choose backgroundcolor
        # GL.glClearColor(0.8, 0.8, 0.8, 1)

        # Remove everything from screen (i.e. displays all white)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        self.grid.rijden()

        # Reset all graphic/shape's position
        GL.glLoadIdentity()

        GL.glRotate(rx, 0, 1, 0)
        GL.glRotate(ry, 1, 0, 0)
        GL.glRotate(rz, 0, 0, 1)

        GL.glTranslate(tx, ty, tz)

        if self.camera.mode == CAMERA_POPPETJE:
            # Move Pepper with the same distances as the self.camera.
            old_pos = self.peper.pos
            self.peper.move(self.peper.pos[0] - diff_pos[0],
                            self.peper.pos[1] - diff_pos[1],
                            self.peper.pos[2] - diff_pos[2])

            angle = angle_between_vectors(old_pos, self.peper.pos)
            if angle:
                print("angle", angle)

            self.peper.rotate(y=self.peper.rotate_pos[1] + angle / 5 *
                              (keys[pygame.K_LEFT] - keys[pygame.K_RIGHT]))

            # *[self.peper.pos[i] + diff_pos[i] for i in range(3)])
            # self.peper.rotate(*[self.peper.rotate_pos[i] + diff_rotate_pos[i]
            #                 for i in range(3)])

        show_coordinates(tx, ty, tz, rx, ry, rz)
        create_line(*list(self.peper.pos[:2]) + [self.peper.pos[2] + 1],
                    *(list(self.peper.pos[:2]) + [0]), (34, 65, 34))

        # GL.glScale(*[1 + self.camera.scale] * 3)
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            #     sys.exit()
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            #     if event.button == 4:
            #         # Zoom in
            #         tz = max(1, tz-1)
            #     elif event.button == 5:
            #         # Zoom out
            #         tz += 1
            #     elif event.button == 1:
            #         # Left
            #         rotate = True
            #     elif event.button == 3:
            #         # Right
            #         move = True
            # elif event.type == pygame.MOUSEBUTTONUP:
            #     if event.button == 1:
            #         rotate = False
            #     elif event.button == 3:
            #         move = False
            # elif event.type == pygame.MOUSEMOTION:
            #     i, j = event.rel
            #     if rotate:
            #         rx += i / 10
            #         ry += j / 10
            #     if move:
            #         tx += i / 100
            #         ty -= j / 100
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                # Switch to Pepper
                self.peper.is_player = True

                print("Move to Pepper")
                print(*self.peper.pos)
                print(*self.peper.rotate_pos)

                # GLU.gluLookAt(*self.camera.pos, *self.peper.pos, 0, 1, 0)

                # Move self.camera to Pepper
                # self.camera.move(x=self.peper.pos[0] - 1,
                #             y=self.peper.pos[1] - 1,
                #             z=self.peper.pos[2] - 0.5)
                # self.camera.rotate(y=270)
                # print(*self.camera.pos)
                # self.camera.rotate(*self.peper.rotate_pos)
                self.camera.mode = CAMERA_POPPETJE

                # When self.camera gets moved, Pepper also should be moved
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                self.peper.is_player = False
                self.camera.mode = CAMERA_FREE


if __name__ == "__main__":
    game = Game()
    clock = pygame.time.Clock()
    while True:
        game.loop()
