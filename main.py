import argparse

from loguru import logger

import games.definitions as d
from games.flaschen_screen import FlaschenScreen
from invaders.game import Game as Invaders
from pong.game import Game as Pong

WIDTH = 64
HEIGHT = 64

parser = argparse.ArgumentParser()

parser.add_argument(
    "-g",
    "--game",
    help="What game do you want to play? 'invaders' or 'pong'?",
    choices=["invaders", "pong"],
    required=True,
)

if __name__ == "__main__":
    # Screen, will show the game state
    screen = FlaschenScreen("localhost", 1337, WIDTH, HEIGHT, transparent=True)

    args = parser.parse_args()
    if args.game == "invaders":
        # Game, it will keep the state of the game
        game = Invaders(screen=screen)
    elif args.game == "pong":
        game = Pong(screen=screen)

    game.loop()

    # Close, clear and say goodbye
    screen.clear_canvas()
    screen.draw_canvas()

    print("bye")
