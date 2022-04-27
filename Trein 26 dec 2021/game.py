import sys
import pygame
import OpenGL.GL as GL
import OpenGL.GLU as GLU
from camera import CAMERA_POPPETJE, Camera
from constants import hex_to_rgb,  show_coordinates
from grid import Grid
from lijnen import create_line
from trein import TREIN_LOCOMOTIEF, TREIN_PASSAGIER

FULL_SCREEN = False

MOVE_STEP = 0.05
ROTATE_STEP = 1
pygame.init()
viewport = (800, 600)
hx = viewport[0]/2
hy = viewport[1]/2

if FULL_SCREEN:
    srf = pygame.display.set_mode(
        viewport, pygame.OPENGL | pygame.DOUBLEBUF | pygame.FULLSCREEN)
else:
    srf = pygame.display.set_mode(
        viewport, pygame.OPENGL | pygame.DOUBLEBUF)


GL.glEnable(GL.GL_COLOR_MATERIAL)
GL.glEnable(GL.GL_DEPTH_TEST)
# most obj files expect to be smooth-shaded
GL.glShadeModel(GL.GL_SMOOTH)


grid = Grid()
camera = Camera()

# pepper = grid.add_poppetje(
#     "Pepper2", "lego_pepper_met_rugzak", rot_x=90, rot_y=180)

pepper = grid.add_poppetje(
    "Pepper", "lego_island2_Pepper_figure", rot_x=90, rot_y=2180, start_x=100)

pop = grid.add_poppetje2(
    "Pop", "hair_001", hex_to_rgb("49332A"), "POST", hex_to_rgb("F00000"),
    "POST", hex_to_rgb("FFFFFF"),
    hex_to_rgb("009cff"), hex_to_rgb("009cff"), hex_to_rgb("009cff"),
    rot_x=90)
# sgm = grid.add_trein("sgm", "sgm", TREIN_LOCOMOTIEF,
#                      start_x=0.5, start_y=1.5, rot_x=90)
# sgm.change_speed(-0.05)

icityvagon = grid.add_trein("f3", "icityvagon", TREIN_PASSAGIER, start_x=0.5,
                            start_y=-2.4, rot_x=90,
                            mtl_images={'Material.006': (True, 'icityvagon6')})

innercity = grid.add_trein("innercity", "innercity", TREIN_LOCOMOTIEF,
                           start_x=0.5, start_y=1.5, rot_x=90,
                           mtl_images={'Material.004': (True, 'innercity6')})
innercity.change_speed(-0.05)

innercity.attach_trein(icityvagon)

# Referentie punt voor deze rijdende trein is (0.5,y=-2.5)
virm1 = grid.add_trein("VIRM3_1", "VIRM3", TREIN_LOCOMOTIEF,
                       start_x=0.5, start_y=2, start_z=0.4, rot_x=90)
virm1.change_speed(0.05)

loco1 = grid.add_trein("Loco1", "lego_loco_kop", TREIN_LOCOMOTIEF,
                       start_x=0.5, start_y=2, start_z=0.3, rot_x=90)
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
                       start_x=2, start_y=2, start_z=0.3, rot_x=90)
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
# sgm.rails = rails4

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

rotate = move = False
points = []
debug = False

while 1:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
            # Switch to Pepper
            pop.is_player = True
            camera.camera_to_poppetje(pop)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            pop.is_player = False
            camera.camera_to_free()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_4:
            camera.camera_to_trein(virm1)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
            debug = not debug

        if camera.mode == CAMERA_POPPETJE:
            pop.handle_event(event)

    keys = pygame.key.get_pressed()
    camera.render(keys)

    tx, ty, tz = camera.pos.get_pos()
    rx, ry, rz = camera.pos.get_rotate()

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
        pop.walk()

    show_coordinates(tx, ty, tz, rx, ry, rz, *
                     (pop.pos.get_pos()), *(pop.pos.get_rotate()))

    for t in grid.locomotieven:
        create_line(t.pos.x, t.pos.y, 5,
                    t.pos.x, t.pos.y, -5, (0.6, 0.6, 0.8))

    if debug:
        points.append(camera.pos.get_pos())

    [create_line(-x, -y, 3, -x, -y, -3, (100, 0, 100))
        for x, y, _ in points]

    # create_line(pop.pos.x, pop.pos.y, 5, pop.pos.x,
    #             pop.pos.y, -5, (200, 0, 200))
    create_line(pop.legs.l_leg.pos.x, pop.legs.l_leg.pos.y, 5,
                pop.legs.l_leg.pos.x,  pop.legs.l_leg.pos.y, -5, (250, 0, 250))
    GL.glScale(*[1 + camera.scale] * 3)
    pygame.display.flip()
