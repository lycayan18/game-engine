from math import hypot


class Vector3:
    def __init__(self, x: float, y: float = None, z: float = None):
        self.x = x
        self.y = y or self.x
        self.z = z or self.y

    def length(self):
        return hypot(self.x, self.y, self.z)

    def calculate_distance(self, another):
        return hypot(self.x - another.x, self.y - another.y, self.z - another.z)

    def __add__(self, another):
        return Vector3(another.x + self.x, another.y + self.y, another.z + self.z)

    def __sub__(self, another):
        return Vector3(self.x - another.x, self.y - another.y, self.z - another.z)

    def __truediv__(self, another):
        return Vector3(self.x / another.x, self.y / another.y, self.z / another.z)

    def __mul__(self, another):
        return Vector3(another.x * self.x, another.y * self.y, another.z * self.z)

    def __eq__(self, another):
        return self.x == another.x and self.y == another.y and self.z == another.z

    def normalize(self):
        length = self.length()

        self.x /= length
        self.y /= length
        self.z /= length

    @staticmethod
    def normalized(vec):
        length = vec.length()

        if length == 0:
            return Vector3(0, 0, 0)

        return vec / Vector3(length)

    @staticmethod
    def distance(a, b):
        return hypot(a.x - b.x, a.y - b.y, a.z - b.z)
