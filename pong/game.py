from timeit import default_timer as timer
from typing import Any, Dict

from games.actor import Actor
from games.base_game import BaseGame
from games.flaschen_screen import FlaschenScreen
from games.gamepad import Gamepad
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
        screen_limits = {
            "top": screen.top + 1,
            "bottom": screen.bottom - 1,
            "right": screen.right,
            "left": screen.left,
        }

        # Player 1 stick
        middle = int(screen.height / 2)
        self.stick_p1 = Stick(x=screen.left, y=middle, screen_limits=screen_limits)
        self.stick_p2 = Stick(x=screen.right, y=middle, screen_limits=screen_limits)

        self.player_1_score = 0
        self.player_2_score = 0

        # The ball
        self.ball = Ball(32, 32, screen_limits=screen_limits)

    def loop(self):
        print("Welcome to Pong!, LED version ;-)")

        gamepad_p1 = Gamepad(joystick="A0", button=None, scale=(0, self.screen.height))
        gamepad_p2 = Gamepad(joystick="A1", button=None, scale=(0, self.screen.height))

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

                if self.ball.left() <= self.screen.left:
                    self.player_2_score += 1

                if self.ball.right() >= self.screen.right:
                    self.player_1_score += 1

                # Draw
                self.screen.clear_canvas()

                next_sprite, start = self.draw_next_sprite(start)

                self.draw(next_sprite=next_sprite)

                if self.player_1_score == 32 or self.player_2_score == 32:
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

        if (
            self.ball.left() <= self.stick_p1.left()
            and self.ball.top() >= self.stick_p1.top()
            and self.ball.bottom() <= self.stick_p1.bottom()
        ):
            self.ball.bounce(direction="right")

        if (
            self.ball.right() >= self.stick_p2.right()
            and self.ball.top() >= self.stick_p2.top()
            and self.ball.bottom() <= self.stick_p2.bottom()
        ):
            self.ball.bounce(direction="left")

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

        self.ball.move(next_sprite=next_sprite)
        self.set_leds(self.ball)

        # Draw a couple of lines on the top and bottom
        for x in range(self.screen.width):
            self.screen.set_in_canvas(x, self.screen.top, (0, 0, 255))
            self.screen.set_in_canvas(x, self.screen.bottom - 1, (0, 0, 255))

        # Draw score
        for x in range(self.player_1_score):
            self.screen.set_in_canvas(x, self.screen.width - 1, (255, 0, 0))

        for x in range(self.player_2_score):
            self.screen.set_in_canvas(
                self.screen.height - x - 1, self.screen.width - 1, (255, 0, 0)
            )

        # Finally, draw the canvas
        self.screen.draw_canvas()
