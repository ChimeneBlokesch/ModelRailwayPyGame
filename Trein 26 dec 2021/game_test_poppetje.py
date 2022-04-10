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
    def __init__(self, full_screen=True):
        pygame.init()

        viewport = (800, 600)

        # hx = viewport[0]/2
        # hy = viewport[1]/2
        if full_screen:
            srf = pygame.display.set_mode(
                viewport, pygame.OPENGL | pygame.DOUBLEBUF | pygame.FULLSCREEN)
        else:
            srf = pygame.display.set_mode(
                viewport, pygame.OPENGL | pygame.DOUBLEBUF)

        GL.glEnable(GL.GL_COLOR_MATERIAL)
        GL.glEnable(GL.GL_DEPTH_TEST)
        # most obj files expect to be smooth-shaded
        GL.glShadeModel(GL.GL_SMOOTH)

        self.grid = Grid()
        self.camera = Camera()

        self.pepper = self.grid.add_poppetje("Pepper", "lego_pepper2",
                                             rot_x=90, rot_y=180)

        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        width, height = viewport
        GLU.gluPerspective(90.0, width/float(height), 1, 100.0)
        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glMatrixMode(GL.GL_MODELVIEW)

        # This is needed for transparency.
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

        self.rondje_rails()
        self.recht_rails()
        self.plaats_treinen()

        self.grid.generate()

    def loop(self):
        pygame.event.pump()
        self.handle_events()

        keys = pygame.key.get_pressed()
        self.camera.render(keys)

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
            # Move Pepper depending on the keys.
            self.pepper.walk()

        show_coordinates(tx, ty, tz, rx, ry, rz, *
                         self.pepper.pos, *self.pepper.rotate_pos)
        create_line(*list(self.pepper.pos[:2]) + [self.pepper.pos[2] + 1],
                    *(list(self.pepper.pos[:2]) + [0]), (34, 65, 34))

        create_line(0, 0, 50, 0, 0, -50, (10, 10, 10))

        GL.glScale(*[1 + self.camera.scale] * 3)
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                # Switch to Pepper
                self.pepper.is_player = True
                self.camera.camera_to_poppetje(self.pepper)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                self.pepper.is_player = False
                self.camera.camera_to_free()
            if self.camera.mode == CAMERA_POPPETJE:
                self.pepper.handle_event(event)

    def plaats_treinen(self):
        icityvagon = self.grid.add_trein("f3", "icityvagon", TREIN_PASSAGIER, start_x=0.5,
                                         start_y=-2.4, rot_x=90,
                                         mtl_images={'Material.006': 'icityvagon6'})

        innercity = self.grid.add_trein("innercity", "innercity", TREIN_LOCOMOTIEF,
                                        start_x=0.5, start_y=1.5, rot_x=90,
                                        mtl_images={'Material.004': 'innercity6'})
        innercity.change_speed(-0.05)

        innercity.attach_trein(icityvagon)

        # Referentie punt voor deze rijdende trein is (0.5,y=-2.5)
        virm1 = self.grid.add_trein("VIRM3_1", "VIRM3", TREIN_LOCOMOTIEF,
                                    start_x=0.5, start_y=2, start_z=0.4, rot_x=90)
        virm1.change_speed(0.05)

        loco1 = self.grid.add_trein("Loco1", "lego_loco_kop", TREIN_LOCOMOTIEF,
                                    start_x=0.5, start_y=2, start_z=0.3, rot_x=90)
        loco1.change_speed(0.1)

        loco2 = self.grid.add_trein("Loco2", "lego_loco_kop", TREIN_LOCOMOTIEF,
                                    start_x=2, start_y=2, start_z=0.3, rot_x=90)
        loco2.change_speed(-0.05)

        loco2.rails = self.grid.rails[17]
        loco1.rails = self.grid.rails[2]
        virm1.rails = self.grid.rails[2]
        innercity.rails = self.grid.rails[3]
        icityvagon.rails = self.grid.rails[2]
        # sgm.rails = self.grid.rails[3]

    def rondje_rails(self):
        rails1 = self.grid.add_bocht("rails1", 45, rotation=0)
        rails1.move(x=-4.5, y=-7)

        rails2 = self.grid.add_bocht("rails2", 45, rotation=45)
        rails2.move(x=0.5, y=-2)

        rails3 = self.grid.add_recht(
            "rails3", is_horizontal=False, go_left_down=True)
        rails3.move(x=0.5)

        rails4 = self.grid.add_recht(
            "rails4", is_horizontal=False, go_left_down=True)
        rails4.move(x=0.5, y=4)

        rails5 = self.grid.add_bocht("rails5", 45, rotation=90)
        rails5.move(x=0.5, y=6)

        rails6 = self.grid.add_bocht("rails6", 45, rotation=135)
        rails6.move(x=-4.5, y=11)

        rails13 = self.grid.add_recht("rails13", go_left_down=False)
        rails13.move(x=-6.5, y=11)

        rails14 = self.grid.add_recht("rails14", go_left_down=False)
        rails14.move(x=-10.5, y=11)

        rails7 = self.grid.add_bocht("rails7", 45, rotation=180)
        rails7.move(x=-12.5, y=11)

        rails8 = self.grid.add_bocht("rails8", 45, rotation=225)
        rails8.move(x=-17.5, y=6)

        rails9 = self.grid.add_recht("rails9", is_horizontal=False)
        rails9.move(x=-17.5, y=4)

        rails10 = self.grid.add_recht("rails10", is_horizontal=False)
        rails10.move(x=-17.5, y=0)

        rails11 = self.grid.add_bocht("rails11", 45, rotation=270)
        rails11.move(x=-17.5, y=-2)

        rails12 = self.grid.add_bocht("rails12", 45, rotation=315)
        rails12.move(x=-12.5, y=-7)

        rails15 = self.grid.add_recht("rails15", go_left_down=True)
        rails15.move(x=-10.5, y=-7)

        rails16 = self.grid.add_recht("rails16", go_left_down=True)
        rails16.move(x=-6.5, y=-7)

        self.grid.connect_45_bochten(rails12, rails11)
        self.grid.connect_rails(rails11, rails10)
        self.grid.connect_rails(rails10, rails9)
        self.grid.connect_rails(rails9, rails8)
        self.grid.connect_45_bochten(rails8, rails7)
        self.grid.connect_rails(rails7, rails14)
        self.grid.connect_rails(rails14, rails13)
        self.grid.connect_rails(rails13, rails6)
        self.grid.connect_45_bochten(rails6, rails5)
        self.grid.connect_rails(rails5, rails4)
        self.grid.connect_rails(rails4, rails3)
        self.grid.connect_rails(rails3, rails2)
        self.grid.connect_45_bochten(rails2, rails1)
        self.grid.connect_rails(rails1, rails16)
        self.grid.connect_rails(rails16, rails15)
        self.grid.connect_rails(rails15, rails12)

    def recht_rails(self):
        rails_1 = self.grid.add_recht("rails_1",
                                      is_horizontal=False, go_left_down=True)
        rails_1.move(2, 6)

        rails_2 = self.grid.add_recht("rails_2",
                                      is_horizontal=False, go_left_down=True)
        rails_2.move(2, 2)

        rails_3 = self.grid.add_recht("rails_3",
                                      is_horizontal=False, go_left_down=True)
        rails_3.move(2, -2)

        self.grid.connect_rails(rails_1, rails_2)
        self.grid.connect_rails(rails_2, rails_3)

    def quit(self):
        sys.exit()


if __name__ == "__main__":
    game = Game(False)
    while True:
        game.loop()
