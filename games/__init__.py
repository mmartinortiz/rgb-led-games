from dataclasses import dataclass
from enum import Enum
from typing import Tuple


class Direction(Enum):
    LEFT: str = "left"
    RIGHT: str = "right"
    UP: str = "up"
    DOWN: str = "down"


Coordinate = Tuple[int, int]


@dataclass
class Rect:
    top_left: Coordinate
    top_right: Coordinate
    bottom_left: Coordinate
    bottom_right: Coordinate
