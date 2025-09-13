import sys
import pygame
import OpenGL.GL as GL
import OpenGL.GLU as GLU
from typing import List


from camera import CAMERA_CHARACTER, Camera
from constants import hex_to_rgb
from grid import Grid
from train import Train, TRAIN_ENGINE, TRAIN_PASSENGER
from position import Position
from character_model import CharacterModel, Hair, Head, Shirt, Arms, Legs
from rails import Straight, Curve

FULL_SCREEN = len(sys.argv) > 1 and sys.argv[1] == "--full_screen"

MOVE_STEP = 0.05
ROTATE_STEP = 1
pygame.init()

viewport = (1920, 1080) if FULL_SCREEN else (800, 600)
hx = viewport[0]/2
hy = viewport[1]/2

flags = pygame.OPENGL | pygame.DOUBLEBUF

if FULL_SCREEN:
    flags |= pygame.FULLSCREEN

srf = pygame.display.set_mode(viewport,  flags)

GL.glEnable(GL.GL_COLOR_MATERIAL)
GL.glEnable(GL.GL_DEPTH_TEST)

# most obj files expect to be smooth-shaded
GL.glShadeModel(GL.GL_SMOOTH)

grid = Grid()
camera = Camera()

pos = Position(rx=90)

hair_color = hex_to_rgb("#E7CD3D")
skin_color = hex_to_rgb("#E7B5A3")
shirt_color = hex_to_rgb("#E7358D")
sleeve_color = hex_to_rgb("#E7358D")
pants_color = hex_to_rgb("#E782AA")
shoes_color = hex_to_rgb("#0C0C0C")

hair = Hair(pos, hair_color, start_z=1.8125)

head = Head(pos, skin_color, start_z=1.1875)

shirt = Shirt(pos, shirt_color, pants_color, start_z=0.75)

arms = Arms(pos, skin_color, sleeve_color, start_z=1.1875)

legs = Legs(pos, pants_color, shoes_color, start_z=0.75)

character = CharacterModel("Player",
                           hair,
                           head,
                           shirt,
                           arms,
                           legs)

grid.add_character(character)

current_character = character

scale_factor = -14.171
scale_factor_curve = 4

straight_rails_length = 10

rails1 = grid.add_curve("rails1", 45, rotation=0)
rails1.move(x=-4.5 * scale_factor_curve, y=-7 * scale_factor_curve)

rails2 = grid.add_curve("rails2", 45, rotation=45)
rails2.move(x=0.5 * scale_factor_curve, y=-2 * scale_factor_curve)

rails3 = grid.add_straight("rails3", is_horizontal=False, go_left_down=True)
rails3.move(x=0.5 * scale_factor)

rails4 = grid.add_straight("rails4", is_horizontal=False, go_left_down=True)
rails4.move(x=0.5 * scale_factor, y=4 * scale_factor)

rails5 = grid.add_curve("rails5", 45, rotation=90)
rails5.move(x=0.5 * scale_factor_curve, y=6 * scale_factor_curve)

rails6 = grid.add_curve("rails6", 45, rotation=135)
rails6.move(x=-4.5 * scale_factor_curve, y=11 * scale_factor_curve)

rails13 = grid.add_straight("rails13", go_left_down=False)
rails13.move(x=-6.5 * scale_factor, y=11 * scale_factor)

rails14 = grid.add_straight("rails14", go_left_down=False)
rails14.move(x=-10.5 * scale_factor, y=11 * scale_factor)

rails7 = grid.add_curve("rails7", 45, rotation=180)
rails7.move(x=-12.5 * scale_factor_curve, y=11 * scale_factor_curve)

rails8 = grid.add_curve("rails8", 45, rotation=225)
rails8.move(x=-17.5 * scale_factor_curve, y=6 * scale_factor_curve)

rails9 = grid.add_straight("rails9", is_horizontal=False)
rails9.move(x=-17.5 * scale_factor, y=4 * scale_factor)

rails10 = grid.add_straight("rails10", is_horizontal=False)
rails10.move(x=-17.5 * scale_factor, y=0)

rails11 = grid.add_curve("rails11", 45, rotation=270)
rails11.move(x=-17.5 * scale_factor_curve, y=-2 * scale_factor_curve)

rails12 = grid.add_curve("rails12", 45, rotation=315)
rails12.move(x=-12.5 * scale_factor_curve, y=-7 * scale_factor_curve)

rails15 = grid.add_straight("rails15", go_left_down=True)
rails15.move(x=-10.5 * scale_factor, y=-7 * scale_factor)

rails16 = grid.add_straight("rails16", go_left_down=True)
rails16.move(x=-6.5 * scale_factor, y=-7 * scale_factor)


grid.connect_45_curves(rails12, rails11)
grid.connect_rails(rails11, rails10)
grid.connect_rails(rails10, rails9)
grid.connect_rails(rails9, rails8)
grid.connect_45_curves(rails8, rails7)
grid.connect_rails(rails7, rails14)
grid.connect_rails(rails14, rails13)
grid.connect_rails(rails13, rails6)
grid.connect_45_curves(rails6, rails5)
grid.connect_rails(rails5, rails4)
grid.connect_rails(rails4, rails3)
grid.connect_rails(rails3, rails2)
grid.connect_45_curves(rails2, rails1)
grid.connect_rails(rails1, rails16)
grid.connect_rails(rails16, rails15)
grid.connect_rails(rails15, rails12)


TRAIN_LENGTH = 12

x = 5
y = 5

engine0 = Train("Engine", "engine", TRAIN_ENGINE,
                start_x=x, start_y=y, rot_x=90)

grid.add_train(engine0)

y += TRAIN_LENGTH

wagon0 = Train("PassengerCar", "passenger_car", TRAIN_PASSENGER,
               start_x=x, start_y=y, rot_x=90)

grid.add_train(wagon0)

engine0.change_speed(-0.05)
engine0.attach_train(wagon0)

engine0.rails = rails3
wagon0.rails = rails3


rails_back_forth: List[Straight | Curve] = []
num_rails = 10
x = 10
cur_y = -straight_rails_length * num_rails / 2

for i in range(num_rails):
    rails = grid.add_straight(f"rails_{i}",
                              is_horizontal=False, go_left_down=True)
    rails.move(x=x, y=cur_y)
    cur_y += straight_rails_length

    if len(rails_back_forth) > 0:
        grid.connect_rails(rails_back_forth[-1], rails)

    rails_back_forth.append(rails)

cur_rails_idx = 2
y = rails_back_forth[cur_rails_idx].pos.y

engine1 = Train("Engine1", "engine", TRAIN_ENGINE,
                start_x=x, start_y=y, rot_x=90)

engine1.rails = rails_back_forth[cur_rails_idx]


cur_rails_idx += 1
y += TRAIN_LENGTH

wagon1 = Train("PassengerCar1", "passenger_car", TRAIN_PASSENGER,
               start_x=x, start_y=y, rot_x=90)


wagon1.rails = rails_back_forth[cur_rails_idx]


cur_rails_idx += 1
y += TRAIN_LENGTH

engine2 = Train("Engine2", "engine", TRAIN_PASSENGER,
                start_x=x, start_y=y, rot_x=90, rot_y=180)

cur_rails_idx += 1
engine2.rails = rails_back_forth[cur_rails_idx]


grid.add_train(engine1)
grid.add_train(wagon1)
grid.add_train(engine2)

engine1.change_speed(0.05)
engine1.attach_train(wagon1)
wagon1.attach_train(engine2)

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
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            current_character.is_player = False
            current_character = None
            camera.camera_to_free()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
            # Switch to character view
            character.is_player = True
            current_character = character
            camera.camera_to_character(current_character)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
            debug = not debug
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_4:
            camera.camera_to_train(engine0)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_5:
            camera.camera_to_train(engine1)

        if camera.mode == CAMERA_CHARACTER:
            current_character.handle_event(event)

    keys = pygame.key.get_pressed()
    camera.render(keys)

    tx, ty, tz = camera.pos.get_pos()
    rx, ry, rz = camera.pos.get_rotate()

    # Choose backgroundcolor
    # GL.glClearColor(0.8, 0.8, 0.8, 1)

    # Remove everything from screen (i.e. displays all white)
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
    grid.drive()

    # Reset all graphic/shape's position
    GL.glLoadIdentity()

    GL.glRotate(rx, 0, 1, 0)
    GL.glRotate(ry, 1, 0, 0)
    GL.glRotate(rz, 0, 0, 1)

    GL.glTranslate(tx, ty, tz)

    if camera.mode == CAMERA_CHARACTER:
        current_character.walk()

    GL.glScale(*[1 + camera.scale] * 3)
    pygame.display.flip()
