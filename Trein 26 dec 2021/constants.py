import numpy as np
import math
from collections import namedtuple

TREINEN_MAP = "treinen/"
RAILS_MAP = "rails/"

Punt = namedtuple("Punt", ["x", "y", "z"])

BREEDTE_RAILS = 5

WIDTH_GRID = 30
HEIGHT_GRID = 25
LENGTE_VAKJE = 2

# Factor to multiply with the train's speed used in curves.
SPEEDUP_BOCHT = 10


def angle_between(p1, p2):
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    return np.rad2deg((ang1 - ang2) % (2 * np.pi))


def angle_between_vectors(x1, y1, x2, y2):
    teller = x1 * x2 + y1 * y2
    noemer = math.sqrt((x1 ** 2 + y1 ** 2)) * math.sqrt((x2 ** 2 + y2 ** 2))

    return math.degrees(math.acos(teller/noemer))


def angle_vector(x, y):
    return math.degrees(np.arctan2(x, y))


def afstand(x1, y1, x2, y2):
    return math.sqrt((x1 - x2)**2 + (y1-y2)**2)


def print_rails_info(rails):
    prev_name = rails.prev.name if rails.prev else None
    next_name = rails.next.name if rails.next else None
    print(rails.name, rails.get_ref_punten(),
          prev_name, next_name)
