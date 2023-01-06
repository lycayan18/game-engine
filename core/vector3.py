from math import sqrt


class Vector3:
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def calculate_distance(self, another):
        return sqrt((self.x - another.x)**2 + (self.y - another.y)**2 + (self.z - another.z)**2)

    def length(self):
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def __add__(self, another):
        return Vector3(another.x + self.x, another.y + self.y, another.z + self.z)

    def __sub__(self, another):
        return Vector3(self.x - another.x, self.y - another.y, self.z - another.z)

    def __div__(self, another):
        return Vector3(self.x / another.x, self.y / another.y, self.z / another.z)

    def __mul__(self, another):
        return Vector3(another.x * self.x, another.y * self.y, another.z * self.z)

    def __eq__(self, another):
        return self.x == another.x and self.y == another.y and self.z == another.z