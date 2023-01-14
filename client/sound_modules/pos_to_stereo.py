from math import sin, cos
from core.vector3 import Vector3
from client.camera import Camera


def global_pos_to_local_pos(pos: Vector3, camera: Camera) -> Vector3:
    """
    Transforms global position to camera-view relative position.
    Just gets direction to global pos, rotates it by camera's Y rotation and that's all.
    """

    rotation = camera.get_rotation().y

    s = sin(rotation)
    c = cos(rotation)

    direction = pos - camera.position

    return Vector3(
        direction.x * c - direction.z * s,
        0.0,
        direction.x * s + direction.z * c
    )


def get_stereo_coefficients_from_position(pos: Vector3, camera: Camera) -> tuple[float, float]:
    """
    Returns left and right channel coefficients from pos and camera.
    Useful for generating stereo effect from space-travelling sounds.
    """

    # Transform global position to camera-view relative position
    local_position = global_pos_to_local_pos(pos, camera)

    direction = Vector3.normalized(local_position)

    distance = Vector3.distance(camera.position, pos)

    left = (1.0 - direction.x) / max(distance * distance, 1.0)
    right = (direction.x + 1.0) / max(distance * distance, 1.0)

    return min(left, 1.0), min(right, 1.0)
