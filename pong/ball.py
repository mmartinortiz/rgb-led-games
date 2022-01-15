from random import randint
from timeit import default_timer as timer

from games.actor import Actor
from pong import ASSETS_PATH


class Ball(Actor):
    """
    An alien, the bad guy of the game
    """

    def __init__(self, x, y, screen_width=None, screen_height=None):
        super().__init__(assets_path=ASSETS_PATH)
        self.load_sprites(sprites_glob=self.get_asset("ball_*.png"))

        self.screen_width = screen_width - 1
        self.screen_height = screen_height - 1

        # Starting position
        self.x = x
        self.y = y

        # Speed
        self.vx = self.rand_speed()
        self.vy = self.rand_speed()

        self.start = timer()

    @staticmethod
    def rand_speed():
        return randint(-3, 3)

    def update(self, button: int):
        # The ball does not care about the user input
        pass

    def move(self, next_sprite):
        # Did we hit a wall?
        if self.x <= 0 or self.x + self.width >= self.screen_width:
            self.vx = -self.vx

        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.vy = -self.vy

        self.x += self.vx
        self.y += self.vy
