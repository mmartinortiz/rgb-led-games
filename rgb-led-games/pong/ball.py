from random import randint

from loguru import logger

from games import Direction
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

    @staticmethod
    def rand_speed(
        current_speed: int = None, minimum: int = -3, maximum: int = 3
    ) -> int:
        """Returns a random spreed between `minimum` and `maximum`. If `current_speed` is passed,
        the sign of the returned speed will be the inverted value. For example, if `current_speed`
        is -3, the returned speed will be between 1 and 3

        Args:
            current_speed (int, optional): Current speed; to be excluded from the returned values. Defaults to None.
            minimum (int, optional): Minimum value to return. Defaults to -3.
            maximum (int, optional): Maximum value to return. Defaults to 3.

        Returns:
            int: A random speed
        """
        if current_speed:
            return randint(1, maximum) if current_speed > 0 else randint(minimum, -1)

        speed = 0
        while speed == 0:
            speed = randint(-minimum, maximum)

        return speed

    def update(self):
        """Update ball position according to its own speed"""
        self.x += self.vx
        self.y += self.vy

    def check_the_walls(self):
        """Check if the ball collides with a wall"""
        if self.left <= self.screen_limits.left:
            self.bounce(Direction.RIGHT, limit=self.screen_limits.left)
        elif self.right >= self.screen_limits.right:
            self.bounce(Direction.LEFT, limit=self.screen_limits.right)
        elif self.top <= self.screen_limits.top:
            self.bounce(Direction.DOWN, limit=self.screen_limits.top)
        elif self.bottom >= self.screen_limits.bottom:
            self.bounce(Direction.UP, limit=self.screen_limits.bottom)

    def check_safe_position(self):
        """Check if the ball is within the screen limits. If it is
        not, its position is corrected to be within the screen limits
        """
        self.x = (
            self.x if self.left >= self.screen_limits.left else self.screen_limits.left
        )
        self.x = (
            self.x
            if self.right <= self.screen_limits.right
            else self.screen_limits.right - self.width
        )
        self.y = (
            self.y if self.top >= self.screen_limits.top else self.screen_limits.top
        )
        self.y = (
            self.y
            if self.bottom <= self.screen_limits.bottom
            else self.screen_limits.bottom - self.height
        )

    def bounce(self, direction: Direction, limit: int, change_angle: bool = False):
        """Update the ball speed and position to simulate a bounce

        Args:
            direction (str): New direction of the ball
            limit (int): Coordinte (`x` or `y`, depending on the direction) describing
            the limits that cannot be passed by the ball
            change_angle (bool, optional): Should the ball change the current angle after bouncing?. Defaults to False.
        """
        if direction is Direction.LEFT:
            self.vx = -self.rand_speed(self.vx) if change_angle else -self.vx
            self.x = limit - self.width + 1
        elif direction is Direction.RIGHT:
            self.vx = -self.rand_speed(self.vx) if change_angle else -self.vx
            self.x = limit
        elif direction is Direction.DOWN:
            self.vy = -self.rand_speed(self.vy) if change_angle else -self.vy
            self.y = limit
        elif direction is Direction.UP:
            self.vy = -self.rand_speed(self.vy) if change_angle else -self.vy
            self.y = limit - self.height + 1
        else:
            logger.error(f"Unknown direction: {direction}")
