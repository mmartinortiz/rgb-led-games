from loguru import logger

from games.actor import Actor
from games.utils import ScreenLimits
from invaders import ASSETS_PATH


class Spaceship(Actor):
    """
    The spaceship is the good guy, the one controlled by the player
    """

    def __init__(self, x: int, y: int, screen_limits: ScreenLimits):
        super().__init__(assets_path=ASSETS_PATH)
        self.load_sprites(sprites_glob=self.get_asset("spaceship_*.png"))

        self.screen_limits = screen_limits

        # Starting position, bottom left
        self.x = x
        self.y = y - self.height if y + self.height > screen_limits.bottom else y

    def update(self, position: int):
        max_position = self.screen_limits.right - self.width

        self.x = position if position <= max_position else max_position
