from loguru import logger

import games.definitions as d
from games.actor import Actor
from invaders import get_asset


class Spaceship(Actor):
    """
    The spaceship is the good guy, the one controlled by the player
    """

    def __init__(self, screen_width=None, screen_height=None):
        super().__init__()
        self.load_sprites(sprites_glob=get_asset("spaceship_*.png"))

        self.screen_width = screen_width
        self.screen_height = screen_height

        # Starting position, bottom left
        self.x = 0
        self.y = screen_height - self.height

    def update(self, position: int):
        max_position = self.screen_width - self.width

        self.x = position if position <= max_position else max_position
        # x = position if position <= max_position else max_position
        # logger.debug(x)
        # if button == d.LEFT:
        #     if self.left() > 0:
        #         # Move to left
        #         self.x -= 1

        # if button == d.RIGHT:
        #     if self.right() < self.screen_width:
        #         # Move to right
        #         self.x += 1
