from math import sqrt


class Vector2:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def length(self):
        return sqrt(self.x * self.x + self.y * self.y)

    def __add__(self, another):
        return Vector2(another.x + self.x, another.y + self.y)

    def __sub__(self, another):
        return Vector2(self.x - another.x, self.y - another.y)

    def __div__(self, another):
        return Vector2(self.x / another.x, self.y / another.y)

    def __mul__(self, another):
        return Vector2(another.x * self.x, another.y * self.y)

    def __eq__(self, another):
        return self.x == another.x and self.y == another.y