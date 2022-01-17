from typing import Dict

from games.actor import Actor
from games.utils import ScreenLimits
from pong import ASSETS_PATH


class Stick(Actor):
    """
    The spaceship is the good guy, the one controlled by the player
    """

    def __init__(self, x, y, screen_limits=ScreenLimits):
        super().__init__(assets_path=ASSETS_PATH)
        self.load_sprites(sprites_glob=self.get_asset("stick_*.png"))

        self.screen_limits = screen_limits

        # Correct position if starting point is out of the boundaries
        self.x = x
        self.y = y

    def update(self, position: int):
        if position <= self.screen_limits.top:
            self.y = self.screen_limits.top
        elif position >= self.screen_limits.bottom - self.height:
            self.y = self.screen_limits.bottom - self.height
        else:
            self.y = position
