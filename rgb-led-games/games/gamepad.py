from typing import Any, Dict, Tuple

from pitop import Button, Potentiometer


class Gamepad:
    def __init__(self, joystick: str, button: str, scale: Tuple[int, int] = None):
        """Returns a gamepad object. A gamepad is composed by two elements:

        - A potentiometer that indicates its position
        - A button

        This GamePad is intended to be used only with the PiTop SDK

        https://pi-top-pi-top-python-sdk.readthedocs-hosted.com/

        Args:
            joystick (str): Port of the potentiometer, for example "A0"
            button (str): Port of the button, for example "D0"
            scale (Tuple[int, int]): If provided, the potentiometer values
            will be scaled between the first and second element of this tuple
        """

        self.joystick = Potentiometer(joystick) if joystick else None
        self.button = Button(button) if button else None

        self.potentiometer_min = 0
        self.potentiometer_max = 999

        self.scale = scale
        if scale:
            self.range_low = scale[0]
            self.range_up = scale[1]

    def get_status(self) -> Dict[str, Any]:
        joystick_value = (
            (
                self.scale_potentiometer_value(self.joystick.position)
                if self.scale
                else self.joystick.position
            )
            if self.joystick
            else None
        )

        button_pressed = self.button.is_pressed if self.button else None

        status = {"joystick": joystick_value, "button": button_pressed}

        return status

    def scale_potentiometer_value(self, value: int) -> int:
        """Scales a given value between another two. Util method to, for example, scale
        the potentiometer value between a given range

        Args:
            value (int): Value to be scaled
            range_low (int): Minimum value of the range where the value will be scaled
            range_up (int): Maximum value of the range

        Returns:
            int: Scaled value
        """

        return int(
            (
                ((self.range_up - self.range_low) * (value - self.potentiometer_min))
                / (self.potentiometer_max - self.potentiometer_min)
            )
            + self.range_low
        )
