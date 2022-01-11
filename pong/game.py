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
        super().__init__()

        # Screen where things are drawn
        self.screen = screen

        # Player 1 stick
        self.stick_p1 = Stick(screen_height=screen.height, screen_width=screen.width)

        # The ball
        self.ball = Ball(32, 32, screen_height=screen.height, screen_width=screen.width)

    def loop(self):
        print("Welcome to Pong!, LED version ;-)")

        gamepad_p1 = Gamepad(joystick="A0", button="D3", scale=(0, self.screen.height))

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

                # Update state
                self.update(player_1)

                # Draw
                self.screen.clear_canvas()

                next_sprite, start = self.draw_next_sprite(start)

                self.draw(next_sprite=next_sprite)
            except KeyboardInterrupt:
                bye = True

    def update(self, user_input: Dict[str, Any]) -> None:
        """
        Update the game status

        Args:
            button (int): Button pressed by the player
        """
        self.stick_p1.update(user_input["joystick"])

        # if collision(self.stick_p1, self.ball):
        # self.ball.bounce()

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
        self.stick_p1.draw(next_sprite=next_sprite)
        self.set_leds(self.stick_p1)

        self.ball.move(next_sprite=next_sprite)
        self.set_leds(self.ball)

        # Finally, draw the canvas
        self.screen.draw_canvas()
