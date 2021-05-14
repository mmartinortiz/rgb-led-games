from games.actor import Actor


class Stick(Actor):
    """
    The spaceship is the good guy, the one controlled by the player
    """

    def __init__(self, screen_width=None, screen_height=None):
        super().__init__()
        self.load_sprites(sprites_glob="./assets/stick_*.png")

        self.screen_width = screen_width
        self.screen_height = screen_height

        # Left side, middle
        self.x = 0
        self.y = 0

    def update(self, position: int):
        max_position = self.screen_height - self.height
        # logger.debug(position)
        self.y = position if position <= max_position else max_position
