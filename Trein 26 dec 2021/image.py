import pygame
import OpenGL.GL as GL

from constants import Punt


def read_image_file(filename):
    surf = pygame.image.load(filename)
    image = pygame.image.tostring(surf, 'RGBA', 1)
    ix, iy = surf.get_rect().size

    # Generate a texture ID
    texid = GL.glGenTextures(1)

    # Make our new texture ID the current 2D texture
    GL.glBindTexture(GL.GL_TEXTURE_2D, texid)

    # Deze zorgt ervoor dat het plaatje weergegeven wordt.
    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER,
                       GL.GL_LINEAR)

    GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER,
                       GL.GL_LINEAR)

    # Deze ook nodig om plaatje te weergeven, als combi
    # Copy the texture data into the current texture ID
    GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, ix, iy,
                    0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, image)

    # Note that only the ID is returned, no reference to the image object
    # or the string data is stored in user space, the data is only present
    # within the GL after this call exits
    return texid, ix, iy


class ImageObject:
    def __init__(self, filename):
        self.filename = filename
        self.gl_list = 0
        self.pos = Punt(0, 0, 0)
        self.rotate_pos = Punt(0, 0, 0)
        self.texture, self.width, self.height = read_image_file(self.filename)
        print("width", self.width)
        print("height", self.height)

    def generate(self):
        self.gl_list = GL.glGenLists(1)
        GL.glNewList(self.gl_list, GL.GL_COMPILE)
        GL.glEnable(GL.GL_TEXTURE_2D)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glFrontFace(GL.GL_CCW)

        GL.glColor(1, 1, 1)

        GL.glBindTexture(GL.GL_TEXTURE_2D,
                         self.texture)

        GL.glBegin(GL.GL_QUADS)

        GL.glTexCoord2f(0, 0)
        GL.glVertex(0, 0, 0)

        GL.glTexCoord2f(1, 0)
        GL.glVertex(0, self.width,  0)

        GL.glTexCoord2f(1, 1)
        GL.glVertex(self.height, self.width, 0)

        GL.glTexCoord2f(0, 1)
        GL.glVertex(self.height, 0,  0)

        GL.glEnd()

        GL.glDisable(GL.GL_TEXTURE_2D)
        GL.glDisable(GL.GL_BLEND)
        GL.glEndList()

    def render(self, pos=None, rotate_pos=None):
        if pos is None:
            pos = self.pos

        if rotate_pos is None:
            rotate_pos = self.rotate_pos

        GL.glPushMatrix()
        GL.glTranslate(pos.x, pos.y, pos.z)
        GL.glRotate(rotate_pos.x, 1, 0, 0)
        GL.glRotate(rotate_pos.y, 0, 1, 0)
        GL.glRotate(rotate_pos.z, 0, 0, 1)
        scale_value = 5 / 87  # nieuw / oud
        # GL.glScale(0.1, 0.1, 1)
        GL.glScale(scale_value, scale_value, 1)
        # self.width *= 0.1  # 8.7
        # self.height *= 0.1  # 2.4
        self.width *= scale_value
        self.height *= scale_value

        print(self.width, self.height)

        GL.glCallList(self.gl_list)
        GL.glPopMatrix()

    def move(self, x=None, y=None, z=None):
        x = x if x is not None else self.pos.x
        y = y if y is not None else self.pos.y
        z = z if z is not None else self.pos.z

        self.pos = Punt(x, y, z)

    def rotate(self, x=None, y=None, z=None):
        x = x if x is not None else self.rotate_pos.x
        y = y if y is not None else self.rotate_pos.y
        z = z if z is not None else self.rotate_pos.z

        self.rotate_pos = Punt(x, y, z)

    def free(self):
        GL.glDeleteLists([self.gl_list])


class ImageObjectEdited(ImageObject):
    def __init__(self, filename, vertices, tex_vertices):
        super().__init__(filename)
        self.vertices = vertices
        self.tex_vertices = tex_vertices

    # Override
    def generate(self):
        self.gl_list = GL.glGenLists(1)
        GL.glNewList(self.gl_list, GL.GL_COMPILE)
        GL.glEnable(GL.GL_TEXTURE_2D)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glFrontFace(GL.GL_CCW)

        GL.glColor(1, 1, 1)

        GL.glBindTexture(GL.GL_TEXTURE_2D,
                         self.texture)

        GL.glBegin(GL.GL_QUADS)

        for i in range(len(self.vertices)):
            GL.glTexCoord2f(*self.tex_vertices[i])
            GL.glVertex(*self.vertices[i])

        GL.glEnd()

        GL.glDisable(GL.GL_TEXTURE_2D)
        GL.glDisable(GL.GL_BLEND)
        GL.glEndList()
