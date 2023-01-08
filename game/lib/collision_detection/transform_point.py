import glm
from core.vector3 import Vector3


def transform_point(point: Vector3, translate: Vector3, rotate: Vector3):
    local = point + translate

    matrix = glm.mat4x4()

    matrix = glm.rotate(matrix, rotate.x, glm.vec3(1.0, 0.0, 0.0))
    matrix = glm.rotate(matrix, rotate.y, glm.vec3(0.0, 1.0, 0.0))
    matrix = glm.rotate(matrix, rotate.z, glm.vec3(0.0, 0.0, 1.0))

    vec = glm.mul(matrix, glm.vec4(local.x, local.y, local.z, 1.0))

    return Vector3(vec.x, vec.y, vec.z)
