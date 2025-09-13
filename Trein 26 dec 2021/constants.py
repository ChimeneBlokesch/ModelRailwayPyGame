import numpy as np
import math
from collections import namedtuple
import pygame
import OpenGL.GL as GL
import OpenGL.GLU as GLU
pygame.init()

TREINEN_MAP = "trains/"
RAILS_MAP = "rails/"
POPPETJES_MAP = "poppetjes/"
CHARACTER_FOLDER = "character/"

BREEDTE_RAILS = 5

WIDTH_GRID = 30
HEIGHT_GRID = 25
LENGTE_VAKJE = 2

# Factor to multiply with the train's speed used in curves.
SPEEDUP_CURVE = 10


FONT = pygame.font.Font(None, 60)
COLOR_ACTIVE = (50, 120, 210)
COLOR_INACTIVE = (255, 255, 255)
COLOR_TEXT = (43, 56, 43)


def angle_between(p1, p2):
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    return np.rad2deg((ang1 - ang2) % (2 * np.pi))


def angle_between_vectors(v1, v2):
    numerator = np.dot(v1, v2)
    denominator = np.linalg.norm(v1) * np.linalg.norm(v2)

    if denominator == 0 or numerator == 0 or np.allclose([denominator], [numerator]):
        return 0

    return math.degrees(math.acos(numerator/denominator))


def angle_vector(x, y):
    return math.degrees(np.arctan2(x, y))


def afstand(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1-y2)**2)


def print_rails_info(rails):
    prev_name = rails.prev.name if rails.prev else None
    next_name = rails.next.name if rails.next else None
    print(rails.name, rails.get_ref_punten(),
          prev_name, next_name)


def show_coordinates(tx, ty, tz, rx, ry, rz, ptx, pty, ptz, prx, pry, prz):
    text = f"{int(tx)} {int(ty)} {int(tz)} {int(rx)} {int(ry)} {int(rz)}       "
    text += f"{int(ptx)} {int(pty)} {int(ptz)} {int(prx)} {int(pry)} {int(prz)}"
    textsurface = FONT.render(text, False, (250, 250, 250))
    textData = pygame.image.tostring(textsurface, "RGBA", True)
    GL.glWindowPos2d(0, 0)
    GL.glDrawPixels(textsurface.get_width(), textsurface.get_height(
    ), GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, textData)


def gamma_correction(r, g, b, gamma=0.45):
    return r ** gamma, g ** gamma, b ** gamma


def hex_to_rgb(hex_str: str):
    """
    Converts a gamma corrected hexadecimal string to not gamma corrected rgb.
    """
    hex_str = hex_str.replace("#", "")
    r = (int(hex_str[:2], base=16) / 255) ** 2.22
    g = (int(hex_str[2:4], base=16) / 255) ** 2.22
    b = (int(hex_str[4:], base=16) / 255) ** 2.22

    return r, g, b


def e2h(x: np.ndarray):
    """
    Euclidean to homogenous coordinates
    """
    if len(x.shape) == 1:
        return np.hstack((x, [1]))

    return np.vstack((x, np.full(x.shape[1], 1)))


def h2e(tx: np.ndarray):
    """
    Homogenous coordinates to Euclidean
    """
    if len(tx.shape) == 1:
        return tx[:-1] / tx[-1]

    return tx[:-1, :] / tx[-1, :]
