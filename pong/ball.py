from random import randint
from timeit import default_timer as timer

from games.actor import Actor


class Ball(Actor):
    """
    An alien, the bad guy of the game
    """

    def __init__(
        self, x, y, screen_width=None, screen_height=None, sprites_per_second=1 / 6
    ):
        super().__init__()
        self.load_sprites(sprites_glob="./assets/ball_*.png")

        self.screen_width = screen_width - 1
        self.screen_height = screen_height - 1

        # Starting position
        self.x = x
        self.y = y

        # Speed
        self.vx = randint(2, 3)
        self.vy = randint(-4, 4)

        self.sprites_per_second = sprites_per_second
        self.start = timer()

    def update(self, button: int):
        # The ball does not care about the user input
        pass

    def move(self, next_sprite):
        if not next_sprite:
            return

        self.x += self.vx
        self.y += self.vy

        # Did we hit a wall?
        if self.x <= 0:
            self.x = 0
            self.vx = -self.vx

        if self.x >= self.screen_width - 1:
            self.x = self.screen_width - 1
            self.vx = -self.vx

        if self.y <= 0:
            self.y = 0
            self.vy = randint(-4, 4)

        if self.y >= self.screen_height - 1:
            self.y = self.screen_height - 1
            self.vy = randint(-4, 4)
