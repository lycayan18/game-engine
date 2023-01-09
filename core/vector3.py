from math import hypot


class Vector3:
    def __init__(self, x: float, y: float = None, z: float = None):
        self.x = x
        self.y = y if y is not None else self.x
        self.z = z if z is not None else self.y

    def length(self):
        return hypot(self.x, self.y, self.z)

    def calculate_distance(self, another):
        return hypot(self.x - another.x, self.y - another.y, self.z - another.z)

    def __add__(self, another):
        return Vector3(another.x + self.x, another.y + self.y, another.z + self.z)

    def __sub__(self, another):
        return Vector3(self.x - another.x, self.y - another.y, self.z - another.z)

    def __truediv__(self, another):
        x = 0
        y = 0
        z = 0

        if another.x != 0:
            x = self.x / another.x

        if another.y != 0:
            y = self.y / another.y

        if another.z != 0:
            z = self.z / another.z

        return Vector3(x, y, z)

    def __mul__(self, another):
        return Vector3(another.x * self.x, another.y * self.y, another.z * self.z)

    def __eq__(self, another):
        return self.x == another.x and self.y == another.y and self.z == another.z

    def normalize(self):
        length = self.length()

        self.x /= length
        self.y /= length
        self.z /= length

    def dot(self, another):
        return self.x * another.x + self.y * another.y + self.z * another.z

    @staticmethod
    def normalized(vec):
        length = vec.length()

        if length == 0:
            return Vector3(0, 0, 0)

        return vec / Vector3(length)

    @staticmethod
    def distance(a, b):
        return hypot(a.x - b.x, a.y - b.y, a.z - b.z)
