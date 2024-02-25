from timeit import default_timer as timer

from games.actor import Actor
from games.utils import ScreenLimits
from invaders import ASSETS_PATH


class Alien(Actor):
    """
    An alien, the bad guy of the game
    """

    def __init__(
        self,
        x: int,
        y: int,
        screen_limits: ScreenLimits,
        sprites_per_second: float = 1 / 6,
    ):
        super().__init__(assets_path=ASSETS_PATH)
        self.load_sprites(sprites_glob=self.get_asset("alien_*.png"))

        self.screen_limits = screen_limits

        # Starting position
        self.x = x
        self.y = y

        self.sprites_per_second = sprites_per_second
        self.start = timer()

    def update(self, button: int):
        # Aliens do not care about the user input
        pass

    def move_left(self):
        """
        Move the alien to the left.

        The movement is done according to the value of "sprites_per_second".
        This attribute indicates the number of sprites per second shown on the scrren.
        """
        if timer() - self.start > self.sprites_per_second:
            self.start = timer()
            if self.left > self.screen_limits.left:
                self.x -= 1

    def move_right(self):
        """
        Move the alien to the right.

        The movement is done according to the value of "sprites_per_second".
        This attribute indicates the number of sprites per second shown on the scrren.
        """
        if timer() - self.start > self.sprites_per_second:
            self.start = timer()
            if self.right < self.screen_limits.right:
                self.x += 1

    def explosion(self):
        """
        Explosions are represented with a different animation
        """
        self.load_sprites(sprites_glob=self.get_asset("alien-explosion_*.png"))

        # Replace the iterator by one that is not cyclic
        self.sprites_it = iter(self.sprites)
