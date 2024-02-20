from itertools import product
from timeit import default_timer as timer
from typing import Any, Dict

from loguru import logger

from games.actor import Actor
from games.base_game import BaseGame
from games.flaschen_screen import FlaschenScreen
from games.gamepad import Gamepad
from games.utils import ScreenLimits
from invaders.army import Army
from invaders.bullet import Bullet
from invaders.spaceship import Spaceship


class Game(BaseGame):
    """
    Class that keeps the state of the game
    """

    def __init__(self, screen: FlaschenScreen):
        super().__init__()
        # Screen where things are drawn
        self.screen = screen

        screen_limits = ScreenLimits(
            top=0, bottom=screen.height - 1, left=0, right=screen.width - 1
        )

        self.screen_limits = screen_limits

        # The spaceship
        self.spaceship = Spaceship(
            x=screen_limits.right / 2,
            y=screen_limits.bottom,
            screen_limits=screen_limits,
        )

        # Bullets, none so far
        self.bullets = []

        # The army of aliens
        self.army = Army(number_of_aliens_per_row=4, screen_limits=screen_limits)

        # Set a delay of 2 seconds between bullets
        # This will slow down the player capacity
        # for shooting
        self.lapse_between_bullets = 2
        self.last_bullet_at = timer() - self.lapse_between_bullets

    def loop(self):
        print("Welcome to Space Invarers, LED version ;-)")
        start = timer()
        # Gamepad, will provide input from the user to the game
        gamepad = Gamepad(joystick="A2", button="D7", scale=(0, self.screen.height))

        bye = False
        while not bye:
            # Mainly, the game loop:
            # 1. Get input from the user
            # 2. Update the game state
            # 3. Draw the new state
            try:
                # User input
                player_1 = gamepad.get_status()

                # Update state
                self.update(player_1)

                # Draw
                self.screen.clear_canvas()

                # Calculate if the next sprite will be drawn
                next_sprite, start = self.draw_next_sprite(start)

                # Ask the game to draw the current state
                self.draw(next_sprite=next_sprite)

                # time.sleep(0.01)

            except KeyboardInterrupt:
                bye = True

    def new_bullet(self, x: int, y: int) -> None:
        """
        Creates a new bullet, at coordinates x and y

        Args:
            x (int): X coordinate for the new bullet
            y (int): Y coordinate for the new bullet
        """
        if timer() - self.last_bullet_at > self.lapse_between_bullets:
            self.last_bullet_at = timer()
            self.bullets.append(Bullet(x=x, y=y, screen_limits=self.screen_limits))

    def update(self, user_input: Dict[str, Any]) -> None:
        """Update the game status according to the use rinput

        Args:
            user_input (Dict[str, Any]): The user input comes from the Gamepad
        """
        # Update spaceship position
        self.spaceship.update(user_input["joystick"])

        # Create new bullets
        if user_input["button"]:
            self.new_bullet(
                x=self.spaceship.left + 2,
                y=self.spaceship.top - 6
                # Todo: calculate coordinates programatically
            )

        # Move the aliens army
        self.army.move_army()

        # Move all the bullets
        for bullet in self.bullets:
            bullet.update(None)

        # Any bullet impacted an alien?
        for bullet, alien in product(self.bullets, self.army.aliens):
            if (
                bullet.top <= alien.bottom
                and bullet.bottom >= alien.top
                and bullet.left >= alien.left
                and bullet.right <= alien.right
            ):
                # Impact! "Hide" the bullet
                bullet.show = False

                # Make the alien explode
                alien.explosion()

        # Update alived aliens and bullets
        self.bullets = [bullet for bullet in self.bullets if bullet.show]
        self.army.update_army()

        # Keep only those bullets that are "in the screen"
        self.bullets = [
            bullet for bullet in self.bullets if bullet.top > self.screen_limits.top
        ]

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
        self.spaceship.draw(next_sprite=next_sprite)
        self.set_leds(self.spaceship)

        # For each alien, activate current sprite and set leds on
        for alien in self.army.aliens:
            alien.draw(next_sprite=next_sprite)
            self.set_leds(alien)

        # Indicate the bullets if it is time to draw the next sprite
        for bullet in self.bullets:
            bullet.draw(next_sprite=next_sprite)
            self.set_leds(bullet)

        # Finally, draw the canvas
        self.screen.draw_canvas()
