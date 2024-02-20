from timeit import default_timer as timer


from games.actor import Actor
from games.utils import ScreenLimits
from invaders import ASSETS_PATH


class Bullet(Actor):
    """
    Bullets are shot by the spaceship
    """

    def __init__(
        self, x: int, y: int, screen_limits: ScreenLimits, sprites_per_second=1 / 6
    ):
        super().__init__(assets_path=ASSETS_PATH)
        self.load_sprites(sprites_glob=self.get_asset("bullet_*.png"))

        self.screen_limits = screen_limits

        self.x = x
        self.y = y
        self.sprites_per_second = sprites_per_second
        self.start = timer()

    def update(self, button: int):
        if timer() - self.start > self.sprites_per_second:
            self.start = timer()
            if (
                self.top > self.screen_limits.top
                and self.bottom < self.screen_limits.bottom
            ):
                self.y -= 1
