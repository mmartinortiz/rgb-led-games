def scale_position(x):
    min_value = 0
    max_value = 1000

    a = 0
    b = 64

    return int((((b - a) * (x - min_value)) / (max_value - min_value)) + a)
