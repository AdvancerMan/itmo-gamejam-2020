EPS = 1e-6


def equals(x: float, y: float) -> bool:
    return abs(x - y) <= EPS


def less(x: float, y: float) -> bool:
    return x < y


def lessOrEquals(x: float, y: float) -> bool:
    return less(x, y) or equals(x, y)
