import os
import pathlib
from abc import ABCMeta, abstractclassmethod
from timeit import default_timer as timer

from loguru import logger


class BaseGame(metaclass=ABCMeta):
    def __init__(self, sprites_per_second: int = 6):
        self.SPS = sprites_per_second

    @abstractclassmethod
    def loop(self):
        ...

    @abstractclassmethod
    def update(self):
        ...

    def draw_next_sprite(self, start) -> bool:
        new_timer = timer()
        return (True, new_timer) if new_timer - start > 1 / self.SPS else (False, start)
