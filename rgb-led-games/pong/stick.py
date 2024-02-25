
from games.actor import Actor
from games.utils import ScreenLimits
from pong import ASSETS_PATH


class Stick(Actor):
    """
    Player representation on the Pong game
    """

    def __init__(self, x, y, screen_limits=ScreenLimits):
        super().__init__(assets_path=ASSETS_PATH)
        self.load_sprites(sprites_glob=self.get_asset("stick_*.png"))

        self.screen_limits = screen_limits

        # Starting position of the stick
        self.x = x
        self.y = y

    def update(self, y: int):
        """Update the stick position accoring to user input and
        screen limits

        Args:
            y (int): New position on y axis
        """
        if y <= self.screen_limits.top:
            self.y = self.screen_limits.top
        elif y >= self.screen_limits.bottom - self.height:
            self.y = self.screen_limits.bottom - self.height
        else:
            self.y = y
