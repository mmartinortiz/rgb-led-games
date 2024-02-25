def scale_position(
    x: int, a: int = 0, b: int = 64, min_value: int = 0, max_value: int = 1000
) -> int:
    """Scales the value of `x` between `a` and `b` given a minimum and
    maximum value of `x`

    Args:
        x (int): Value to be scaled.
        a (int, optional): Lower limit. Defaults to 0.
        b (int, optional): Upper limit. Defaults to 64.
        min_value (int, optional): Minimum value that `x` can have. Defaults to 0.
        max_value (int, optional): Maximum value that `x` can have. Defaults to 1000.

    Returns:
        int: Scaled value
    """

    return int((((b - a) * (x - min_value)) / (max_value - min_value)) + a)
