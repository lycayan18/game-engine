from core.vector3 import Vector3


class Shape:
    def __init__(self, position: Vector3 = None, rotation: Vector3 = None):
        self.position = position or Vector3(0)
        self.rotation = rotation or Vector3(0)

    def set_position(self, position: Vector3):
        self.position = position

    def set_rotation(self, rotation: Vector3):
        self.rotation = rotation

    def get_position(self) -> Vector3:
        return self.position

    def get_rotation(self) -> Vector3:
        return self.rotation

    def collide_point(self, point: Vector3) -> bool:
        return (point.x == self.position.x and
                point.y == self.position.y and
                point.z == self.position.z)
