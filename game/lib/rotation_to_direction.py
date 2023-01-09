from core.vector3 import Vector3
import glm


def rotation_to_direction(rotation: Vector3) -> Vector3:
    vec = glm.vec3(0.0, 0.0, 1.0)

    vec = glm.rotateX(vec, rotation.x)
    vec = glm.rotateY(vec, rotation.y)
    vec = glm.rotateZ(vec, rotation.z)

    return Vector3(vec.x, vec.y, vec.z)
