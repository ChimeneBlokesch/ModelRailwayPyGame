from OpenGL import GL

from constants import HEIGHT_GRID, LENGTE_VAKJE, WIDTH_GRID
from helper import BLUE, PURPLE, RED, create_line


GREEN = (0.027, 0.529, 0.027)

ground_vertices = (
    (-WIDTH_GRID, HEIGHT_GRID, -0.1),
    (WIDTH_GRID, HEIGHT_GRID, -0.1),
    (WIDTH_GRID, -HEIGHT_GRID, -0.1),
    (-WIDTH_GRID, -HEIGHT_GRID, -0.1),
)

# top left
# top right
# bottom right
# bottom left


def create_ground():
    GL.glBegin(GL.GL_QUADS)
    GL.glColor3fv(GREEN)

    for vertex in ground_vertices:
        GL.glVertex3fv(vertex)

    GL.glEnd()


def create_grid():
    min_length = min(WIDTH_GRID, HEIGHT_GRID)

    for i in range(0, min_length, LENGTE_VAKJE):
        # Vertical
        create_line(i,  HEIGHT_GRID, 0, i,  -HEIGHT_GRID, 0, PURPLE)
        create_line(-i, HEIGHT_GRID, 0, -i,  -HEIGHT_GRID, 0, PURPLE)

        # Horizontal
        create_line(WIDTH_GRID,  i, 0, -WIDTH_GRID,  i, 0, PURPLE)
        create_line(WIDTH_GRID,  -i, 0,  -WIDTH_GRID, -i,  0, PURPLE)

    if WIDTH_GRID == HEIGHT_GRID:
        return

    end = min_length - min_length % LENGTE_VAKJE

    if WIDTH_GRID > HEIGHT_GRID:
        for i in range(end, WIDTH_GRID, LENGTE_VAKJE):
            # Vertical
            create_line(i,  HEIGHT_GRID, 0, i,  -HEIGHT_GRID, 0, PURPLE)
            create_line(-i, HEIGHT_GRID, 0, -i,  -HEIGHT_GRID, 0, PURPLE)
    elif HEIGHT_GRID < WIDTH_GRID:
        for i in range(WIDTH_GRID, HEIGHT_GRID, LENGTE_VAKJE):
            # Horizontal
            create_line(WIDTH_GRID,  i, 0, -WIDTH_GRID,  i, 0, PURPLE)
            create_line(WIDTH_GRID,  -i, 0,  -WIDTH_GRID, -i,  0, PURPLE)


def create_grid_lines():
    create_line(-100, 0, 0, 100, 0, 0, RED)
    create_line(0, -100, 0, 0, 100, 0, BLUE)
    create_line(0, 0, -100, 0, 0, 100, GREEN)
