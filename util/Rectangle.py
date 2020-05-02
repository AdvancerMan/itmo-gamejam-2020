class Rectangle:
    def __init__(self, x: float, y: float, width: float, height: float):
        self.x = x
        self.y = y
        self.w = width
        self.h = height

    def size(self) -> tuple:
        return self.w, self.h

    def pos(self) -> tuple:
        return self.x, self.y

    def getX(self) -> float:
        return self.x

    def getY(self) -> float:
        return self.y

    def getWidth(self) -> float:
        return self.w

    def getHeight(self) -> float:
        return self.h

    def union(self, other):
        # other: Rect
        self.x = min(self.x, other.x)
        self.y = min(self.y, other.y)
        self.w = max(self.w, other.w)
        self.h = max(self.h, other.h)
        return self

    def move(self, x, y):
        self.x += x
        self.y += y
        return self

    def __str__(self):
        return str((self.x, self.y, self.w, self.h))

    def intersects(self, other) -> bool:
        # other: Rectangle
        return intersects(self.x, self.x + self.w, other.x, other.x + other.w) \
               and intersects(self.y, self.y + self.h, other.y, other.y + other.h)


def rectFromTwoPoints(x1: float, y1: float, x2: float, y2: float) -> Rectangle:
    return Rectangle(x1, y1, x2 - x1, y2 - y1)


def rectFromSize(x: float, y: float, width: float, height: float) -> Rectangle:
    return Rectangle(x, y, width, height)


def intersects(s1: float, f1: float, s2: float, f2: float) -> bool:
    return max(s1, s2) <= min(f1, f2)
