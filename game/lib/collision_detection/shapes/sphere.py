from math import sqrt
from core.vector3 import Vector3
from game.lib.collision_detection.shapes.shape import Shape
from game.lib.collision_detection.transform_point import transform_point


def ray_sphere_intersection(ray_origin: Vector3, ray_direction: Vector3, sphere_center: Vector3, sphere_radius: float):
    """
    Returns distance to intersection point in ray direction if line intersects sphere and None otherwise.\n
    I don't know what happens here ¯\\\\_(ツ)_/¯
    """

    oc = ray_origin - sphere_center

    b = Vector3.dot(oc, ray_direction)
    c = Vector3.dot(oc, oc) - sphere_radius * sphere_radius

    height_squared = b * b - c

    if height_squared < 0.0:  # no interesection
        return None

    height = sqrt(height_squared)

    if -b - height > 0:
        return -b - height
    else:
        return -b + height


class Sphere(Shape):
    def __init__(self, radius: float = 1.0, position: Vector3 = None, rotation: Vector3 = None):
        super(Sphere, self).__init__(position, rotation)

        self.radius = radius

    def collide_point(self, point: Vector3) -> bool:
        return Vector3.distance(point, self.position) <= self.radius

    def line_intersection(self, a: Vector3, b: Vector3) -> Vector3:
        direction = Vector3.normalized(b - a)

        distance = ray_sphere_intersection(
            a, direction, self.position, self.radius)

        # Check that intersection point lies on a segment ( distance > 0 and distance < line segment length )
        if distance is not None and distance > 0 and distance < Vector3.distance(a, b):
            return a + direction * Vector3(distance)

        return None
