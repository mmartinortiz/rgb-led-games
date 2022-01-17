from random import randint
from timeit import default_timer as timer
from typing import Dict

from loguru import logger

from games.actor import Actor
from games.utils import ScreenLimits
from pong import ASSETS_PATH


class Ball(Actor):
    """
    An alien, the bad guy of the game
    """

    def __init__(self, x: int, y: int, screen_limits: ScreenLimits):
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
    def rand_speed(current_speed: int = None):
        if current_speed:
            return randint(1, 3) if current_speed > 0 else randint(-3, -1)

        speed = 0
        while speed == 0:
            speed = randint(-3, 3)

        return speed

    def update(self, button: int = None):
        self.x += self.vx
        self.y += self.vy

    def check_the_walls(self):
        if self.left() <= self.screen_limits.left:
            self.bounce("right", limit=self.screen_limits.left)
        elif self.right() >= self.screen_limits.right:
            self.bounce("left", limit=self.screen_limits.right)
        elif self.top() <= self.screen_limits.top:
            self.bounce("down", limit=self.screen_limits.top)
        elif self.bottom() >= self.screen_limits.bottom:
            self.bounce("up", limit=self.screen_limits.bottom)

    def check_safe_position(self):
        self.x = (
            self.x
            if self.left() >= self.screen_limits.left
            else self.screen_limits.left
        )
        self.x = (
            self.x
            if self.right() <= self.screen_limits.right
            else self.screen_limits.right - self.width
        )
        self.y = (
            self.y if self.top() >= self.screen_limits.top else self.screen_limits.top
        )
        self.y = (
            self.y
            if self.bottom() <= self.screen_limits.bottom
            else self.screen_limits.bottom - self.height
        )

    def bounce(self, direction: str, limit: int, change_angle: bool = False):
        if direction == "left":
            self.vx = -self.rand_speed(self.vx) if change_angle else -self.vx
            self.x = limit - self.width + 1
        elif direction == "right":
            self.vx = -self.rand_speed(self.vx) if change_angle else -self.vx
            self.x = limit
        elif direction == "down":
            self.vy = -self.rand_speed(self.vy) if change_angle else -self.vy
            self.y = limit
        elif direction == "up":
            self.vy = -self.rand_speed(self.vy) if change_angle else -self.vy
            self.y = limit - self.height + 1
        else:
            logger.error(f"Unknown direction: {direction}")
