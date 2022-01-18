from timeit import default_timer as timer
from typing import Any, Dict

from loguru import logger

from games import Direction
from games.base_game import BaseGame
from games.colors import BLUE, PALE_RED, PALE_WHITE, RED, Color
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

        # Animation for the impact of the ball
        self.left_impact = False
        self.right_impact = False

        # Maximum score. Once the score is reach, the game restarts
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
                # Determine if a new sprite needs to be drawn
                next_sprite, start = self.draw_next_sprite(start)

                # Clear the canvas before we starting drawing
                self.screen.clear_canvas()

                self.draw(next_sprite=next_sprite)

                # Check if any of the players have scored
                if self.ball.left() <= self.screen.left:
                    self.player_2_score += 1
                    self.left_impact = True

                if self.ball.right() >= self.screen.right:
                    self.player_1_score += 1
                    self.right_impact = True

                # Did anybory win?
                if (
                    self.player_1_score == self.max_score
                    or self.player_2_score == self.max_score
                ):
                    # We have a winer! and start again :-)
                    self.player_1_score = self.player_2_score = 0

            except KeyboardInterrupt:
                bye = True

    def update(self, player_1: Dict[str, Any], player_2: Dict[str, Any]) -> None:
        """Update the game status with the player's input

        Args:
            player_1 (Dict[str, Any]): Player 1 input
            player_2 (Dict[str, Any]): Player 2 input
        """
        # Update sticks position
        self.stick_p1.update(player_1["joystick"])
        self.stick_p2.update(player_2["joystick"])

        # Update the ball position
        self.ball.update()

        # Check if the ball has hit one of the sticks
        if (
            self.ball.left() <= self.stick_p1.right()
            and self.ball.bottom() >= self.stick_p1.top()
            and self.ball.top() <= self.stick_p1.bottom()
        ):
            self.ball.bounce(
                direction=Direction.RIGHT,
                limit=self.stick_p1.right(),
                change_angle=True,
            )

        if (
            self.ball.right() >= self.stick_p2.left()
            and self.ball.bottom() >= self.stick_p2.top()
            and self.ball.top() <= self.stick_p2.bottom()
        ):
            self.ball.bounce(
                direction=Direction.LEFT, limit=self.stick_p2.left(), change_angle=True
            )

        # Check if the ball hits the wall
        self.ball.check_the_walls()

        # Correct the ball position if needed
        self.ball.check_safe_position()

    def draw_impact(self, x: int, color: Color = PALE_WHITE):
        """Draws an animation to show the impact of the ball in a wall

        Args:
            x (int): Position of the x axis where the impact happen
        """
        for y in range(self.screen_limits.top, self.screen_limits.bottom):
            self.screen.set_in_canvas(x, y, color)

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
            self.draw_impact(self.screen_limits.left)
            self.left_impact = False

        if self.right_impact:
            self.draw_impact(self.screen_limits.right)
            self.right_impact = False

        # Draw a couple of lines on the top and bottom
        for x in range(self.screen.width):
            self.screen.set_in_canvas(x, self.screen.top, BLUE)
            self.screen.set_in_canvas(x, self.screen.bottom - 1, BLUE)
            self.screen.set_in_canvas(x, self.screen.bottom, PALE_RED)

        # Draw score
        self.screen.set_in_canvas(31, self.screen.width - 1, BLUE)
        self.screen.set_in_canvas(32, self.screen.width - 1, BLUE)
        for x in range(self.player_1_score):
            self.screen.set_in_canvas(x, self.screen.width - 1, RED)

        for x in range(self.player_2_score):
            self.screen.set_in_canvas(
                self.screen.height - x - 1, self.screen.width - 1, RED
            )

        # Finally, draw the canvas
        self.screen.draw_canvas()
