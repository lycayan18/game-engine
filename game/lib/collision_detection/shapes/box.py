from core.vector3 import Vector3
from game.lib.collision_detection.shapes.shape import Shape
from game.lib.collision_detection.transform_point import transform_point


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
