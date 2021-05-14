from typing import NamedTuple
from loguru import logger
from collections import namedtuple

from pong.actor import Actor

Rectangle = namedtuple('Rectangle', ['top_left', 'top_right', 'bottom_left', 'bottom_right'])

def scale_position(x):
    min_value = 0
    max_value = 1000

    a = 0
    b = 64

    return int((((b - a) * (x - min_value)) / (max_value - min_value)) + a)


def collision(a: Actor, b: Actor) -> bool:
    """Detects if there is a collision between two actors

    Args:
        a (Actor): Actor A
        b (Actor): Actor B

    Returns:
        bool: True if both actors collide
    """
    rect_a = Rectangle(a.x, a.x + a.width, a.y, a.y + a.height)
    rect_b = Rectangle(b.x, b.x + b.width, b.y, b.y + b.height)

    if rect_a.top_left >= rect_b.top_left and rect_a.top_left <= rect_b.top_right:
        return True

    if rect_a.top_right >= rect_b.top_left and rect_a.top_right <= rect_b.top_right:
        return True

    if rect_a.bottom_left >= rect_b.bottom_left and rect_b.bottom_left <= rect_b.bottom_right:
        return True

    return False
