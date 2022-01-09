import sys
import pygame
import OpenGL.GL as GL
import OpenGL.GLU as GLU
from grid import Grid
from lijnen import create_line

pygame.init()
viewport = (800, 600)
hx = viewport[0]/2
hy = viewport[1]/2
srf = pygame.display.set_mode(viewport, pygame.OPENGL | pygame.DOUBLEBUF)


GL.glEnable(GL.GL_COLOR_MATERIAL)
GL.glEnable(GL.GL_DEPTH_TEST)
# most obj files expect to be smooth-shaded
GL.glShadeModel(GL.GL_SMOOTH)


# virm2 = Trein("VIRM3_2", "VIRM3.obj")
# virm2.generate()


grid = Grid()

# Referentie punt voor deze rijdende trein is (0.5,y=-2.5)
# virm1 = grid.add_trein("VIRM3_1", "VIRM3.obj", 0.5, -1.5)
# virm1.rotate(x=90)  # Nutteloos?
# # virm1.move(x=0.75, z=0.91)
# # x is horizontaal
# # y is verticaal
# # z is hoogte
# virm1.move(x=0.5, y=3.5, z=1)
# virm1.change_speed(0.05)

# TODO:Change ref punt
loco1 = grid.add_trein("Loco1", "lego_loco_kop.obj", 0.5, 0.5)
loco1.move(x=0.5, y=2, z=0.755)
# loco1.rotate(z=90)
loco1.change_speed(0.05)

rails1 = grid.add_bocht(45, rotation=0)
rails1.move(x=-4.5, y=-7)

rails2 = grid.add_bocht(45, rotation=45)
rails2.move(x=0.5, y=-2)

rails3 = grid.add_recht(is_horizontal=False, go_left_down=True,
                        ref_punt_prev=(0, 2), ref_punt_next=(0, -2))
rails3.move(x=0.5)

rails4 = grid.add_recht(is_horizontal=False, go_left_down=True,
                        ref_punt_prev=(0, 2), ref_punt_next=(0, -2))
rails4.move(x=0.5, y=4)

rails5 = grid.add_bocht(45, rotation=90)
rails5.move(x=0.5, y=6)

rails6 = grid.add_bocht(45, rotation=135)
rails6.move(x=-4.5, y=11)

rails7 = grid.add_bocht(45, rotation=180)
rails7.move(x=-4.5, y=11)

rails8 = grid.add_bocht(45, rotation=225)
rails8.move(x=-9.5, y=6)

rails9 = grid.add_recht(is_horizontal=False,
                        ref_punt_prev=(0, -2), ref_punt_next=(0, 2))
rails9.move(x=-9.5, y=4)

rails10 = grid.add_recht(is_horizontal=False,
                         ref_punt_prev=(0, -2), ref_punt_next=(0, 2))
rails10.move(x=-9.5, y=0)

rails11 = grid.add_bocht(45, rotation=270)
rails11.move(x=-9.5, y=-2)

rails12 = grid.add_bocht(45, rotation=315)
rails12.move(x=-4.5, y=-7)

grid.connect_45_bochten(rails12, rails11)
grid.connect_rails(rails11, rails10)
grid.connect_rails(rails10, rails9)
grid.connect_rails(rails9, rails8)
grid.connect_45_bochten(rails8, rails7)
grid.connect_rails(rails7, rails6)
grid.connect_45_bochten(rails6, rails5)
grid.connect_rails(rails5, rails4)
grid.connect_rails(rails4, rails3)
grid.connect_rails(rails3, rails2)
grid.connect_45_bochten(rails2, rails1)
grid.connect_rails(rails1, rails12)

grid.generate()
loco1.rails = rails3
print("rails1", rails1.get_ref_punten())
print("rails2", rails2.get_ref_punten())
print("rails3", rails3.get_ref_punten())
print("rails11", rails11.get_ref_punten())
print("rails12", rails12.get_ref_punten())
clock = pygame.time.Clock()

GL.glMatrixMode(GL.GL_PROJECTION)
GL.glLoadIdentity()
width, height = viewport
GLU.gluPerspective(90.0, width/float(height), 1, 100.0)
GL.glEnable(GL.GL_DEPTH_TEST)
GL.glMatrixMode(GL.GL_MODELVIEW)


rx, ry = (0, -50)
tx, ty = (0, 0)
zpos = 15
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
                # zpos -= 1
                zpos = max(1, zpos-1)
            elif event.button == 5:
                zpos += 1
            elif event.button == 1:
                rotate = True
            elif event.button == 3:
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

    # Choose backgroundcolor
    # GL.glClearColor(0.8, 0.8, 0.8, 1)

    # Remove everything from screen (i.e. displays all white)
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

    # Reset all graphic/shape's position
    GL.glLoadIdentity()

    GL.glTranslate(tx * 10, ty * 10, - zpos)

    GL.glRotate(rx, 0, 1, 0)
    GL.glRotate(ry, 1, 0, 0)

    # grid.render()
    grid.rijden()

    virm1_x, virm1_y = loco1.get_ref_punt()
    print(loco1.get_ref_punt())
    create_line(virm1_x, virm1_y, 5, virm1_x, virm1_y, -5, (0.8, 0.3, 0.6))
    create_line(loco1.pos[0], loco1.pos[1], 5,
                loco1.pos[0], loco1.pos[1], -5, (0.6, 0.6, 0.8))

    pygame.display.flip()
