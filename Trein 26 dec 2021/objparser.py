import os
import numpy as np
import pygame
import OpenGL.GL as GL
import sqlite3

from constants import TREINEN_MAP, gamma_correction


IMAGE_PREFIX = "image_"


class Object3D:
    def __init__(self, folder, obj_name, swap_yz=False):
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []
        self.gl_list = 0
        self.swap_yz = swap_yz
        self.folder = folder
        self.obj_name = obj_name
        self.read_obj_file(folder + obj_name + ".obj")

    def change_img(self, mtl_images):
        for mtl_name in mtl_images.keys():
            # Set image.
            filename = mtl_images[mtl_name] + ".png"
            self.mtl[mtl_name]["map_Kd"] = filename
            self.mtl[mtl_name]["map_d"] = filename
            imagefile = os.path.join(TREINEN_MAP, filename)
            image = self.read_image_file(imagefile)
            self.mtl[mtl_name][IMAGE_PREFIX + "map_Kd"] = image
            self.mtl[mtl_name][IMAGE_PREFIX + "map_d"] = image

    def update_db(self):
        conn = sqlite3.connect("treinen.db")
        cursor = conn.cursor()
        try:
            cursor.execute(
                """INSERT INTO soort VALUES(null, ?, 3)""", (self.obj_name,))
        except sqlite3.IntegrityError:
            ...

        for m in self.mtl:
            if "map_Kd" not in self.mtl[m]:
                continue

            cursor.execute("""SELECT id from soort where name = ?""",
                           (self.obj_name,))
            trein = cursor.fetchall()[0][0]
            cursor.execute("""SELECT id from plaatjes where name = ?""",
                           (self.mtl[m]["map_Kd"],))
            img = cursor.fetchall()[0][0]

            try:
                cursor.execute("""
                    INSERT INTO materialen(name, img, trein) VALUES(?,?,?)""",
                               (m, img, trein))
            except sqlite3.IntegrityError:
                ...

        conn.commit()
        conn.close()

    def read_obj_file(self, filename):
        material = None
        dirname = os.path.dirname(filename)

        with open(filename) as f:
            for line in f.readlines():
                if line.startswith("#") or not line:
                    # Ignore line
                    continue

                line = line.rstrip().split()

                if line[0] == "mtllib":
                    self.mtl = self.read_mtl_file(
                        os.path.join(dirname, line[1]))

                    if not self.obj_name.startswith('bocht') and not self.obj_name.startswith('recht'):
                        self.update_db()
                    continue

                if line[0] in ["v", "vn"]:
                    self.add_vector(line[0], line[1:4])
                    continue

                if line[0] == "vt":
                    self.add_vector(line[0], line[1:3])
                    continue

                if line[0] in ["usemtl", "usemat"]:
                    material = line[1]

                if line[0] == "f":
                    self.add_face(line[1:], material)

    def read_mtl_file(self, filename):
        contents = {}
        mtl = None
        dirname = os.path.dirname(filename)

        for line in open(filename, "r"):
            if line.startswith('#'):
                continue

            line = line.split()

            if not line:
                continue

            if line[0] == 'newmtl':
                # Contents wordt bijgewerkt door de mtl variable.
                mtl = contents[line[1]] = {}
                continue

            if mtl is None:
                raise ValueError("mtl file doesn't start with newmtl stmt")

            type_map = line[0]

            try:
                mtl[type_map] = list(map(float, line[1:]))
            except ValueError:
                # Value is name of file
                name = "_".join(line[1:])
                mtl[type_map] = name
                imagefile = os.path.join(dirname, name)
                mtl[IMAGE_PREFIX + type_map] = self.read_image_file(imagefile)

        return contents

    def read_image_file(self, filename):
        try:
            surf = pygame.image.load(filename).convert_alpha()
        except FileNotFoundError:
            print(filename, "not found")
            exit()
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
        return texid

    def add_vector(self, type, values):
        v = list(map(float, values))

        if not "vt" and self.swap_yz:
            v = v[0], v[2], v[1]

        if type == "v":
            self.vertices.append(v)
        elif type == "vn":
            self.normals.append(v)
        elif type == "vt":
            self.texcoords.append(v)

    def add_face(self, values, material):
        face = []
        norms = []
        texcoords = []

        for v in values:
            w = v.split('/')
            face.append(int(w[0]))

            if len(w) >= 2 and len(w[1]) > 0:
                texcoords.append(int(w[1]))
            else:
                texcoords.append(0)

            if len(w) >= 3 and len(w[2]) > 0:
                norms.append(int(w[2]))
            else:
                norms.append(0)

        self.faces.append((face, norms, texcoords, material))

    def generate(self):
        self.gl_list = GL.glGenLists(1)
        GL.glNewList(self.gl_list, GL.GL_COMPILE)
        GL.glEnable(GL.GL_TEXTURE_2D)
        GL.glFrontFace(GL.GL_CCW)

        for face in self.faces:
            vertices, normals, texture_coords, material = face
            mtl = self.mtl[material]
            GL.glColor(1, 1, 1)

            if IMAGE_PREFIX + "map_Kd" in mtl:
                # use diffuse texmap
                GL.glBindTexture(GL.GL_TEXTURE_2D,
                                 mtl[IMAGE_PREFIX + 'map_Kd'])
            else:
                # use diffuse color, because this is the mostly used color
                texid = GL.glGenTextures(1)
                GL.glBindTexture(GL.GL_TEXTURE_2D, texid)
                GL.glColor(gamma_correction(*mtl['Kd']))

            GL.glBegin(GL.GL_POLYGON)

            for i in range(len(vertices)):
                if normals[i] > 0:
                    GL.glNormal3fv(self.normals[normals[i] - 1])

                if texture_coords[i] > 0:
                    GL.glTexCoord2fv(self.texcoords[texture_coords[i] - 1])

                GL.glVertex3fv(self.vertices[vertices[i] - 1])

            GL.glEnd()

        GL.glDisable(GL.GL_TEXTURE_2D)
        GL.glEndList()

    def render(self, pos, flip=False,
               scale_value=(1, 1, 1)):
        GL.glPushMatrix()
        GL.glTranslate(pos.x, pos.y, pos.z)
        GL.glRotate(pos.rx, 1, 0, 0)
        GL.glRotate(pos.ry, 0, 1, 0)
        GL.glRotate(pos.rz, 0, 0, 1)

        if flip:
            GL.glScale(1, -1, 1)

        # y=scale_value * ((x-1) ** 1 + x | 0)
        # Blijkbaar werkt dit niet samen :(
        GL.glScale(*scale_value)
        GL.glCallList(np.array(self.gl_list))
        GL.glPopMatrix()

    def free(self):
        GL.glDeleteLists([self.gl_list])
