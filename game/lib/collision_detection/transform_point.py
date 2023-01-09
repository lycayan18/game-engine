import glm
from core.vector3 import Vector3


def transform_point(point: Vector3, translate: Vector3, rotate: Vector3):
    local = point + translate

    vec = glm.vec3(local.x, local.y, local.z)

    vec = glm.rotateX(vec, rotate.x)
    vec = glm.rotateY(vec, rotate.y)
    vec = glm.rotateZ(vec, rotate.z)

    return Vector3(vec.x, vec.y, vec.z)
