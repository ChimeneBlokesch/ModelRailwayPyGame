# class Lijn:
#     def __init__(self, x,y,width,height):
#         self.x = x
#         self.y = y
#         self.width=width
#         self.height=height

#     def generate(self):

import OpenGL.GL as GL

PURPLE = (0.752, 0.278, 0.960)
RED = (0.819, 0.062, 0.152)
BLUE = (0.062, 0.133, 0.819)
GREEN = (0.109, 0.819, 0.062)


def create_line(x, y, z, x2, y2, z2, color):
    GL.glColor(color)
    GL.glBegin(GL.GL_LINES)

    GL.glVertex3fv((x, y, z))
    GL.glVertex3fv((x2, y2, z2))

    GL.glEnd()
