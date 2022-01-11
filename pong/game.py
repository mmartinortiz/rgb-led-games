from timeit import default_timer as timer

from games.actor import Actor
from games.base_game import BaseGame
from games.flaschen_screen import FlaschenScreen
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

        start = timer()

        bye = False
        while not bye:
            # Mainly, the game loop:
            # 1. Get input from the user
            # 2. Update the game state
            # 3. Draw the new state
            try:
                # User input
                player_1 = self.stick_p1.get_status()

                # Update state
                self.update(player_1)

                # Draw
                next_sprite, start = self.draw_next_sprite(start)

                self.draw(next_sprite=next_sprite)
            except KeyboardInterrupt:
                bye = True

    def update(self, button: int) -> None:
        """
        Update the game status

        Args:
            button (int): Button pressed by the player
        """
        # Update spaceship
        if button is not None:
            self.stick_p1.update(button)

        # if collision(self.stick_p1, self.ball):
        # self.ball.bounce()

    def set_leds(self, actor: Actor) -> None:
        """
        For a given actor, set on the leds on the screen according
        to the current sprite

        Args:
            actor (Actor): Actor to be drawn in the screen
        """

        # j --> y
        for j, row in enumerate(actor.current_sprite):
            # i --> x
            for i, color in enumerate(row):
                rgb = (color[0], color[1], color[2])

                x = i + actor.x
                y = j + actor.y

                self.screen.set_in_canvas(x, y, rgb)

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
