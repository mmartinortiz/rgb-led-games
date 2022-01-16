from typing import Dict

from games.actor import Actor
from pong import ASSETS_PATH


class Stick(Actor):
    """
    The spaceship is the good guy, the one controlled by the player
    """

    def __init__(self, x, y, screen_limits=Dict[str, str]):
        super().__init__(assets_path=ASSETS_PATH)
        self.load_sprites(sprites_glob=self.get_asset("stick_*.png"))

        self.screen_limits = screen_limits

        # Correct position if starting point is out of the boundaries
        self.x = (
            screen_limits["right"] - self.width + 1
            if x + self.width > screen_limits["right"]
            else x
        )
        self.y = (
            screen_limits["bottom"] - self.height + 1
            if y + self.height > screen_limits["bottom"]
            else y
        )

    def update(self, position: int):
        if position <= self.screen_limits["top"]:
            self.y = self.screen_limits["top"]
        elif position >= self.screen_limits["bottom"] - self.height:
            self.y = self.screen_limits["bottom"] - self.height
        else:
            self.y = position
