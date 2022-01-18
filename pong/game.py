from timeit import default_timer as timer
from typing import Any, Dict

from loguru import logger

from games.base_game import BaseGame
from games.flaschen_screen import FlaschenScreen
from games.gamepad import Gamepad
from games.utils import ScreenLimits
from pong.ball import Ball
from pong.stick import Stick


class Game(BaseGame):
    """
    Class that keeps the state of the game
    """

    def __init__(self, screen: FlaschenScreen):
        super().__init__(sprites_per_second=10)

        # Screen where things are drawn
        self.screen = screen
        screen_limits = ScreenLimits(
            top=screen.top + 1,
            bottom=screen.bottom - 1,
            right=screen.right,
            left=screen.left,
        )

        self.screen_limits = screen_limits

        # Player 1 stick
        middle = int(screen.height / 2)
        self.stick_p1 = Stick(x=screen.left + 1, y=middle, screen_limits=screen_limits)
        self.stick_p2 = Stick(x=screen.right - 2, y=middle, screen_limits=screen_limits)

        self.player_1_score = 0
        self.player_2_score = 0

        # The ball
        self.ball = Ball(32, 32, screen_limits=screen_limits)

        self.left_impact = False
        self.right_impact = False

        self.max_score = 31

    def loop(self):
        print("Welcome to Pong!, LED version ;-)")

        gamepad_p1 = Gamepad(joystick="A2", button=None, scale=(0, self.screen.height))
        gamepad_p2 = Gamepad(joystick="A3", button=None, scale=(0, self.screen.height))

        start = timer()

        bye = False
        while not bye:
            # Mainly, the game loop:
            # 1. Get input from the user
            # 2. Update the game state
            # 3. Draw the new state
            try:
                # User input
                player_1 = gamepad_p1.get_status()
                player_2 = gamepad_p2.get_status()

                # Update state
                self.update(player_1, player_2)

                # Draw
                next_sprite, start = self.draw_next_sprite(start)
                self.screen.clear_canvas()

                self.draw(next_sprite=next_sprite)

                if self.ball.left() <= self.screen.left:
                    self.player_2_score += 1
                    self.left_impact = True

                if self.ball.right() >= self.screen.right:
                    self.player_1_score += 1
                    self.right_impact = True

                if (
                    self.player_1_score == self.max_score
                    or self.player_2_score == self.max_score
                ):
                    # We have a winer! and start again :-)
                    self.player_1_score = self.player_2_score = 0

            except KeyboardInterrupt:
                bye = True

    def update(self, player_1: Dict[str, Any], player_2: Dict[str, Any]) -> None:
        """
        Update the game status

        Args:
            button (int): Button pressed by the player
        """
        self.stick_p1.update(player_1["joystick"])
        self.stick_p2.update(player_2["joystick"])

        self.ball.update()

        if (
            self.ball.left() <= self.stick_p1.right()
            and self.ball.bottom() >= self.stick_p1.top()
            and self.ball.top() <= self.stick_p1.bottom()
        ):
            self.ball.bounce(
                direction="right", limit=self.stick_p1.right(), change_angle=True
            )

        if (
            self.ball.right() >= self.stick_p2.left()
            and self.ball.bottom() >= self.stick_p2.top()
            and self.ball.top() <= self.stick_p2.bottom()
        ):
            self.ball.bounce(
                direction="left", limit=self.stick_p2.left(), change_angle=True
            )

        self.ball.check_the_walls()
        self.ball.check_safe_position()

    def draw_impact(self, x):
        for y in range(self.screen_limits["top"], self.screen_limits["bottom"]):
            self.screen.set_in_canvas(x, y, (200, 200, 200))

    def draw(self, next_sprite: bool) -> None:
        """
        Draw the game status in the screen. Drawing is composed of
        two steps for each actor:

        1. If `next_sprite` then make active the next sprite
           as the current sprite
        2. Set on the leds according to the current sprite

        Args:
            next_sprite (bool): Is it time to draw the next sprite?
        """
        # Indicate the spachip if it is time to draw the next sprite
        for stick in [self.stick_p1, self.stick_p2]:
            stick.draw(next_sprite=next_sprite)
            self.set_leds(stick)

        self.set_leds(self.ball)

        if self.left_impact:
            self.draw_impact(self.screen_limits["left"])
            self.left_impact = False

        if self.right_impact:
            self.draw_impact(self.screen_limits["right"])
            self.right_impact = False

        # Draw a couple of lines on the top and bottom
        for x in range(self.screen.width):
            self.screen.set_in_canvas(x, self.screen.top, (0, 0, 255))
            self.screen.set_in_canvas(x, self.screen.bottom - 1, (0, 0, 255))
            self.screen.set_in_canvas(x, self.screen.bottom, (50, 0, 0))

        # Draw score
        self.screen.set_in_canvas(31, self.screen.width - 1, (0, 0, 255))
        self.screen.set_in_canvas(32, self.screen.width - 1, (0, 0, 255))
        for x in range(self.player_1_score):
            self.screen.set_in_canvas(x, self.screen.width - 1, (255, 0, 0))

        for x in range(self.player_2_score):
            self.screen.set_in_canvas(
                self.screen.height - x - 1, self.screen.width - 1, (255, 0, 0)
            )

        # Finally, draw the canvas
        self.screen.draw_canvas()
