import numpy as np
from collections import namedtuple

TREINEN_MAP = "treinen/"
RAILS_MAP = "rails/"

Punt = namedtuple("Punt", ["x", "y", "z"])

BREEDTE_RAILS = 5

WIDTH_GRID = 30
HEIGHT_GRID = 25
LENGTE_VAKJE = 2


def angle_between(p1, p2):
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    return np.rad2deg((ang1 - ang2) % (2 * np.pi))
