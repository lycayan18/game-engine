from math import atan2, pi, hypot
from core.vector3 import Vector3


class Camera:
    def __init__(self, fov: float = 90.0, near: float = 0.1, far: float = 100.0, position: Vector3 = Vector3(0.0, 0.0, 0.0), rotation: Vector3 = Vector3(0.0, 0.0, 0.0)):
        self.fov = fov
        self.position = position
        self.rotation = rotation
        self.near = near
        self.far = far

    def set_position(self, position: Vector3):
        self.position = position

    def set_rotation(self, rotation: Vector3):
        self.rotation = rotation

    def get_position(self) -> Vector3:
        return self.position

    def get_rotation(self) -> Vector3:
        return self.rotation

    def set_z_far(self, far: float):
        self.far = far

    def set_z_near(self, near: float):
        self.near = near

    def set_fov(self, fov: float):
        self.fov = fov

    def look_at(self, position: Vector3):
        direction = Vector3.normalized(position - self.position)

        self.rotation.y = -atan2(direction.z, direction.x) + pi * 0.5
        self.rotation.x = atan2(
            hypot(direction.x, direction.z), direction.y) - pi * 0.5
