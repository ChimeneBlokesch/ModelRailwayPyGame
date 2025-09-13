#!/usr/bin/env python
# Basic OBJ file viewer. needs objloader from:
#  http://www.pygame.org/wiki/OBJFileLoader
# LMB + move: rotate
# RMB + move: pan
# Scroll wheel: zoom in/out
import sys
import pygame
import OpenGL.GL as GL
import OpenGL.GLU as GLU

# IMPORT OBJECT LOADER
from objparser import Object3D

pygame.init()
viewport = (800, 600)
hx = viewport[0]/2
hy = viewport[1]/2
srf = pygame.display.set_mode(viewport, pygame.OPENGL | pygame.DOUBLEBUF)

# GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION,  (-40, 200, 100, 0.0))
# GL.glLightfv(GL.GL_LIGHT0, GL.GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
# GL.glLightfv(GL.GL_LIGHT0, GL.GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
# GL.glEnable(GL.GL_LIGHT0)
# GL.glEnable(GL.GL_LIGHTING)
GL.glEnable(GL.GL_COLOR_MATERIAL)
GL.glEnable(GL.GL_DEPTH_TEST)
# most obj files expect to be smooth-shaded
GL.glShadeModel(GL.GL_SMOOTH)

# LOAD OBJECT AFTER PYGAME INIT
print("Folder", sys.argv[1])
print("obj name", sys.argv[2])
virm = Object3D(sys.argv[1], sys.argv[2])
virm.generate()

clock = pygame.time.Clock()

GL.glMatrixMode(GL.GL_PROJECTION)
GL.glLoadIdentity()
width, height = viewport
GLU.gluPerspective(90.0, width/float(height), 1, 100.0)
GL.glEnable(GL.GL_DEPTH_TEST)
GL.glMatrixMode(GL.GL_MODELVIEW)

rx, ry = (0, 0)
tx, ty = (0, 0)
zpos = 5
rotate = move = False
while 1:
    clock.tick(30)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            sys.exit()
        elif e.type == pygame.MOUSEBUTTONDOWN:
            if e.button == 4:
                zpos -= 0.2
                # zpos = max(1, zpos-1)
            elif e.button == 5:
                zpos += 1
            elif e.button == 1:
                rotate = True
            elif e.button == 3:
                move = True
        elif e.type == pygame.MOUSEBUTTONUP:
            if e.button == 1:
                rotate = False
            elif e.button == 3:
                move = False
        elif e.type == pygame.MOUSEMOTION:
            i, j = e.rel
            if rotate:
                rx += i
                ry += j
            if move:
                tx += i
                ty -= j

    # Choose backgroundcolor
    GL.glClearColor(0.8, 0.8, 0.8, 1)

    # Remove everything from screen (i.e. displays all white)
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

    # Reset all graphic/shape's position
    GL.glLoadIdentity()

    # RENDER OBJECT
    GL.glTranslate(tx/20., ty/20., - zpos)
    GL.glRotate(ry, 1, 0, 0)
    GL.glRotate(rx, 0, 1, 0)
    # obj.render()
    virm.render()

    pygame.display.flip()
