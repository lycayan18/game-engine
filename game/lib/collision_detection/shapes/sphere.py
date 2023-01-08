from core.vector3 import Vector3
from game.lib.collision_detection.shapes.shape import Shape
from game.lib.collision_detection.transform_point import transform_point


class Sphere(Shape):
    def __init__(self, radius: float = 1.0, position: Vector3 = None, rotation: Vector3 = None):
        super(Sphere, self).__init__(position, rotation)

        self.radius = radius

    def collide_point(self, point: Vector3) -> bool:
        return Vector3.distance(point, self.positoin) <= self.radius
