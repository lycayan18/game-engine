from typing import Union

from core.vector3 import Vector3
from game.lib.collision_detection.shapes.shape import Shape
from game.lib.collision_detection.transform_point import transform_point


def intersect_AABB_line(ray_origin: Vector3, ray_direction: Vector3, box_size: Vector3) -> Union[float, None]:
    """
    Returns intersection point of a line and Axis Aligned Bounding Box if box and lines intersect and None otherwise.
    """

    m = Vector3(1.0) / ray_direction
    n = m * ray_origin
    k = Vector3(abs(m.x), abs(m.y), abs(m.z)) * box_size

    t1 = n * Vector3(-1) - k
    t2 = n * Vector3(-1) + k

    t_near = max(max(t1.x, t1.y), t1.z)
    t_far = min(min(t2.x, t2.y), t2.z)

    if t_near > t_far or t_far < 0.0:
        return None

    if t_near > 0.0:
        return t_near
    else:
        return t_far


class Box(Shape):
    def __init__(self, size: Vector3 = None, position: Vector3 = None, rotation: Vector3 = None):
        super(Box, self).__init__(position, rotation)

        self.size = size or Vector3(1)

    def collide_point(self, point: Vector3) -> bool:
        local = transform_point(point, self.position *
                                Vector3(-1), self.rotation)

        return (
                local.x >= -self.size.x and
                local.x <= self.size.x and
                local.y >= -self.size.y and
                local.y <= self.size.y and
                local.z >= -self.size.z and
                local.z <= self.size.z
        )

    def line_intersection(self, a: Vector3, b: Vector3) -> Vector3:
        # Transform line points into box-local coordinates, so we can calculate intersection as
        # this box was AABB ( Axis Aligned Bounding Box )
        local_a = transform_point(a, self.position * Vector3(-1),
                                  self.rotation)

        local_b = transform_point(b, self.position * Vector3(-1),
                                  self.rotation)

        direction = Vector3.normalized(local_b - local_a)

        distance = intersect_AABB_line(local_a, direction, self.size)

        if distance is not None and 0.0 < distance < Vector3.distance(a, b):
            return a + Vector3.normalized(b - a) * Vector3(distance)
