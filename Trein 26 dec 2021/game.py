import sys
import pygame
import OpenGL.GL as GL
import OpenGL.GLU as GLU
from constants import print_rails_info, show_coordinates
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

sgm = grid.add_trein("sgm", "sgm", TREIN_LOCOMOTIEF,
                     start_x=0.5, start_y=1.5, rot_x=90)
# sgm.change_speed(-0.05)

icityvagon = grid.add_trein("f3", "icityvagon", TREIN_PASSAGIER, start_x=0.5,
                            start_y=-2.4, rot_x=90,
                            mtl_images={'Material.006': 'icityvagon6'})

innercity = grid.add_trein("innercity", "innercity", TREIN_LOCOMOTIEF,
                           start_x=0.5, start_y=1.5, rot_x=90,
                           mtl_images={'Material.004': 'innercity6'})
innercity.change_speed(-0.05)

innercity.attach_trein(icityvagon)

# Referentie punt voor deze rijdende trein is (0.5,y=-2.5)
virm1 = grid.add_trein("VIRM3_1", "VIRM3", TREIN_LOCOMOTIEF,
                       start_x=0.5, start_y=2, start_z=0.4, rot_x=90)
virm1.change_speed(0.05)

loco1 = grid.add_trein("Loco1", "lego_loco_kop", TREIN_LOCOMOTIEF,
                       start_x=0.5, start_y=2, start_z=0.5, rot_x=90)
loco1.change_speed(0.1)

rails1 = grid.add_bocht("rails1", 45, rotation=0)
rails1.move(x=-4.5, y=-7)

rails2 = grid.add_bocht("rails2", 45, rotation=45)
rails2.move(x=0.5, y=-2)

rails3 = grid.add_recht("rails3", is_horizontal=False, go_left_down=True)
rails3.move(x=0.5)

rails4 = grid.add_recht("rails4", is_horizontal=False, go_left_down=True)
rails4.move(x=0.5, y=4)

rails5 = grid.add_bocht("rails5", 45, rotation=90)
rails5.move(x=0.5, y=6)

rails6 = grid.add_bocht("rails6", 45, rotation=135)
rails6.move(x=-4.5, y=11)

rails13 = grid.add_recht("rails13", go_left_down=False)
rails13.move(x=-6.5, y=11)

rails14 = grid.add_recht("rails14", go_left_down=False)
rails14.move(x=-10.5, y=11)

rails7 = grid.add_bocht("rails7", 45, rotation=180)
rails7.move(x=-12.5, y=11)

rails8 = grid.add_bocht("rails8", 45, rotation=225)
rails8.move(x=-17.5, y=6)

rails9 = grid.add_recht("rails9", is_horizontal=False)
rails9.move(x=-17.5, y=4)

rails10 = grid.add_recht("rails10", is_horizontal=False)
rails10.move(x=-17.5, y=0)

rails11 = grid.add_bocht("rails11", 45, rotation=270)
rails11.move(x=-17.5, y=-2)

rails12 = grid.add_bocht("rails12", 45, rotation=315)
rails12.move(x=-12.5, y=-7)

rails15 = grid.add_recht("rails15", go_left_down=True)
rails15.move(x=-10.5, y=-7)

rails16 = grid.add_recht("rails16", go_left_down=True)
rails16.move(x=-6.5, y=-7)


grid.connect_45_bochten(rails12, rails11)
grid.connect_rails(rails11, rails10)
grid.connect_rails(rails10, rails9)
grid.connect_rails(rails9, rails8)
grid.connect_45_bochten(rails8, rails7)
grid.connect_rails(rails7, rails14)
grid.connect_rails(rails14, rails13)
grid.connect_rails(rails13, rails6)
grid.connect_45_bochten(rails6, rails5)
grid.connect_rails(rails5, rails4)
grid.connect_rails(rails4, rails3)
grid.connect_rails(rails3, rails2)
grid.connect_45_bochten(rails2, rails1)
grid.connect_rails(rails1, rails16)
grid.connect_rails(rails16, rails15)
grid.connect_rails(rails15, rails12)

# for r in grid.rails:
#     print_rails_info(r)

loco2 = grid.add_trein("Loco2", "lego_loco_kop", TREIN_LOCOMOTIEF,
                       start_x=2, start_y=2, start_z=0.5, rot_x=90)
loco2.change_speed(-0.05)

rails_1 = grid.add_recht("rails_1",
                         is_horizontal=False, go_left_down=True)
rails_1.move(2, 6)

rails_2 = grid.add_recht("rails_2",
                         is_horizontal=False, go_left_down=True)
rails_2.move(2, 2)

rails_3 = grid.add_recht("rails_3",
                         is_horizontal=False, go_left_down=True)
rails_3.move(2, -2)

grid.connect_rails(rails_1, rails_2)
grid.connect_rails(rails_2, rails_3)

loco2.rails = rails_2
loco1.rails = rails3
virm1.rails = rails3
innercity.rails = rails4
icityvagon.rails = rails3
sgm.rails = rails4

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

tx, ty, tz = (0, 0, 15)
rx, ry, rz = (0, -90, 0)  # (0, 0) is bovenaanzicht
scale = 0

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

    keys = pygame.key.get_pressed()
    SPEEDUP_STEP = 1 + 2 * keys[pygame.K_RSHIFT]

    # Move to left or right
    tx += SPEEDUP_STEP * MOVE_STEP * \
        (keys[pygame.K_LEFT] - keys[pygame.K_RIGHT]) * \
        math.cos(math.radians(rz))

    ty += SPEEDUP_STEP * MOVE_STEP * \
        (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * \
        math.sin(math.radians(rz))

    # Rotate around point of grid
    rz += SPEEDUP_STEP * ROTATE_STEP * \
        (keys[pygame.K_COMMA] - keys[pygame.K_PERIOD])

    # Move further, back
    if not keys[pygame.K_LCTRL]:
        ty += SPEEDUP_STEP * 0.5 * MOVE_STEP * \
            (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * \
            math.cos(math.radians(rz))

        tx += SPEEDUP_STEP * 0.5 * MOVE_STEP * \
            (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * \
            math.sin(math.radians(rz))

    # Move up or down
    tz += SPEEDUP_STEP * MOVE_STEP * \
        (keys[pygame.K_PAGEUP] - keys[pygame.K_PAGEDOWN])

    # Rotate up or down
    ry += SPEEDUP_STEP * ROTATE_STEP * keys[pygame.K_LCTRL] * \
        (keys[pygame.K_UP] - keys[pygame.K_DOWN])

    # Choose backgroundcolor
    # GL.glClearColor(0.8, 0.8, 0.8, 1)

    # Remove everything from screen (i.e. displays all white)
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
    grid.rijden()

    # Reset all graphic/shape's position
    GL.glLoadIdentity()

    rx = rx % 360
    ry = ry % 360
    rz = rz % 360
    GL.glRotate(rx, 0, 1, 0)
    GL.glRotate(ry, 1, 0, 0)
    GL.glRotate(rz, 0, 0, 1)

    GL.glTranslate(tx * 10, ty * 10, -tz)

    show_coordinates(tx*10, ty*10, -tz, rx, ry, rz)

    # for t in grid.treinen:
    for t in grid.locomotieven:
        # trein_x, trein_y = t.pos[:2]
        # print(t.name, trein_x, trein_y)
        # create_line(trein_x, trein_y, 5, trein_x, trein_y, -5, (0.8, 0.3, 0.6))
        create_line(t.pos[0], t.pos[1], 5,
                    t.pos[0], t.pos[1], -5, (0.6, 0.6, 0.8))

    scale += (keys[pygame.K_z] - keys[pygame.K_x]) * 0.05
    # print([1 + (keys[pygame.K_z] - keys[pygame.K_x]) * 0.05] * 3)
    # GL.glScale(*[1 + (keys[pygame.K_z] - keys[pygame.K_x]) * 0.05] * 3)
    GL.glScale(*[1 + scale] * 3)
    pygame.display.flip()
