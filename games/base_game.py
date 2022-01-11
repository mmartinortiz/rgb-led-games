from abc import ABCMeta, abstractclassmethod
from timeit import default_timer as timer

from loguru import logger

from games.actor import Actor


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

    def set_leds(self, actor: Actor) -> None:
        """
        For a given actor, set on the leds on the screen according
        to the current sprite

        Args:
            actor (Actor): Actor to be drawn in the screen
        """

        # j --> y
        for j, row in enumerate(actor.current_sprite):
            # i --> x
            for i, color in enumerate(row):
                rgb = (color[0], color[1], color[2])

                x = i + actor.x
                y = j + actor.y

                self.screen.set_in_canvas(x, y, rgb)
