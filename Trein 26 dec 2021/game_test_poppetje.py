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
pygame.init()
viewport = (800, 600)
hx = viewport[0]/2
hy = viewport[1]/2
srf = pygame.display.set_mode(viewport, pygame.OPENGL | pygame.DOUBLEBUF)


GL.glEnable(GL.GL_COLOR_MATERIAL)
GL.glEnable(GL.GL_DEPTH_TEST)
# most obj files expect to be smooth-shaded
GL.glShadeModel(GL.GL_SMOOTH)


grid = Grid()
camera = Camera()

pepper = grid.add_poppetje("Pepper", "lego_pepper2", rot_x=90, rot_y=180)

grid.generate()
clock = pygame.time.Clock()

GL.glMatrixMode(GL.GL_PROJECTION)
GL.glLoadIdentity()
width, height = viewport
GLU.gluPerspective(90.0, width/float(height), 1, 100.0)
GL.glEnable(GL.GL_DEPTH_TEST)
GL.glMatrixMode(GL.GL_MODELVIEW)

# This is needed for transparency.
GL.glEnable(GL.GL_BLEND)
GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

tx, ty, tz = 0, 0, 0
rx, ry, rz = 0, 0, 0
rotate = move = False

while 1:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
                # Zoom in
                tz = max(1, tz-1)
            elif event.button == 5:
                # Zoom out
                tz += 1
            elif event.button == 1:
                # Left
                rotate = True
            elif event.button == 3:
                # Right
                move = True
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                rotate = False
            elif event.button == 3:
                move = False
        elif event.type == pygame.MOUSEMOTION:
            i, j = event.rel
            if rotate:
                rx += i / 10
                ry += j / 10
            if move:
                tx += i / 100
                ty -= j / 100
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
            # Switch to Pepper
            pepper.is_player = True

            print("Move to Pepper")
            print(*pepper.pos)
            print(*pepper.rotate_pos)

            GLU.gluLookAt(*camera.pos, *pepper.pos, 0, 1, 0)

            # Move camera to Pepper
            # camera.move(x=pepper.pos[0] - 1,
            #             y=pepper.pos[1] - 1,
            #             z=pepper.pos[2] - 0.5)
            # camera.rotate(y=270)
            # print(*camera.pos)
            # camera.rotate(*pepper.rotate_pos)
            camera.mode = CAMERA_POPPETJE

            # When camera gets moved, Pepper also should be moved
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            pepper.is_player = False
            camera.mode = CAMERA_FREE

    keys = pygame.key.get_pressed()
    diff_pos, diff_rotate_pos = camera.render(keys)
    # print("HIER", diff_pos, diff_rotate_pos, camera.mode)

    tx, ty, tz = camera.pos
    rx, ry, rz = camera.rotate_pos

    # Choose backgroundcolor
    # GL.glClearColor(0.8, 0.8, 0.8, 1)

    # Remove everything from screen (i.e. displays all white)
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
    grid.rijden()

    # Reset all graphic/shape's position
    GL.glLoadIdentity()

    GL.glRotate(rx, 0, 1, 0)
    GL.glRotate(ry, 1, 0, 0)
    GL.glRotate(rz, 0, 0, 1)

    GL.glTranslate(tx, ty, tz)
    if camera.mode == CAMERA_POPPETJE:
        old_pos = pepper.pos
        pepper.move(pepper.pos[0] - diff_pos[0],
                    pepper.pos[1] - diff_pos[1],
                    pepper.pos[2] - diff_pos[2])

        angle = angle_between_vectors(old_pos, pepper.pos)
        if angle:
            print("angle", angle)

        pepper.rotate(y=pepper.rotate_pos[1] + angle / 5 *
                      (keys[pygame.K_LEFT] - keys[pygame.K_RIGHT]))
        GLU.gluLookAt(*camera.pos, *pepper.pos, 1, 1, 0)

        # *[pepper.pos[i] + diff_pos[i] for i in range(3)])
        # pepper.rotate(*[pepper.rotate_pos[i] + diff_rotate_pos[i]
        #                 for i in range(3)])

    show_coordinates(tx, ty, tz, rx, ry, rz)
    create_line(*list(pepper.pos[:2]) + [pepper.pos[2] + 1],
                *(list(pepper.pos[:2]) + [0]), (34, 65, 34))

    GL.glScale(*[1 + camera.scale] * 3)
    pygame.display.flip()
