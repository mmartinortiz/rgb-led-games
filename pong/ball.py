from random import randint
from timeit import default_timer as timer
from typing import Dict

from games.actor import Actor
from pong import ASSETS_PATH


class Ball(Actor):
    """
    An alien, the bad guy of the game
    """

    def __init__(self, x: int, y: int, screen_limits: Dict[str, str]):
        super().__init__(assets_path=ASSETS_PATH)
        self.load_sprites(sprites_glob=self.get_asset("ball_*.png"))

        self.screen_limits = screen_limits

        # Starting position
        self.x = x
        self.y = y

        # Speed
        self.vx = self.rand_speed()
        self.vy = self.rand_speed()

        self.start = timer()

    @staticmethod
    def rand_speed():
        speed = 0
        while speed == 0:
            speed = randint(-3, 3)

        return speed

    def update(self, button: int):
        # The ball does not care about the user input
        pass

    def move(self, next_sprite):
        # Did we hit a wall?
        if (
            self.left() <= self.screen_limits["left"]
            or self.right() >= self.screen_limits["right"]
        ):
            self.vx = -self.vx

        if (
            self.top() <= self.screen_limits["top"]
            or self.bottom() >= self.screen_limits["bottom"]
        ):
            self.vy = -self.vy

        self.x += self.vx
        self.y += self.vy

    def bounce(self, direction: str):
        if direction == "left" or direction == "right":
            self.vx = -self.vx

        if direction == "up" or direction == "down":
            self.vy = -self.vy

        self.x += self.vx
        self.y += self.vy
