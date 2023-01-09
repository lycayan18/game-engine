from pythree import Geometry
from core.vector3 import Vector3


def generate_box(size: Vector3 = Vector3(1)) -> Geometry:
    return Geometry(
        vertices=[
            # Front
            -size.x,  size.y, size.z,
            -size.x, -size.y, size.z,
            +size.x, -size.y, size.z,
            +size.x, -size.y, size.z,
            +size.x,  size.y, size.z,
            -size.x,  size.y, size.z,

            # Back
            -size.x,  size.y, -size.z,
            -size.x, -size.y, -size.z,
            +size.x, -size.y, -size.z,
            +size.x, -size.y, -size.z,
            +size.x,  size.y, -size.z,
            -size.x,  size.y, -size.z,

            # Left
            size.x,  size.y, -size.z,
            size.x, -size.y, -size.z,
            size.x, -size.y,  size.z,
            size.x, -size.y,  size.z,
            size.x,  size.y,  size.z,
            size.x,  size.y, -size.z,

            # Right
            -size.x,  size.y, -size.z,
            -size.x, -size.y, -size.z,
            -size.x, -size.y,  size.z,
            -size.x, -size.y,  size.z,
            -size.x,  size.y,  size.z,
            -size.x,  size.y, -size.z,

            # Top
            -size.x, size.y,  size.z,
            -size.x, size.y, -size.z,
            +size.x, size.y, -size.z,
            +size.x, size.y, -size.z,
            +size.x, size.y,  size.z,
            -size.x, size.y,  size.z,

            # Bottom
            -size.x, -size.y,  size.z,
            -size.x, -size.y, -size.z,
            +size.x, -size.y, -size.z,
            +size.x, -size.y, -size.z,
            +size.x, -size.y,  size.z,
            -size.x, -size.y,  size.z,
        ],
        uvs=[
            # Front
            0.0, 1.0,
            0.0, 0.0,
            1.0, 0.0,
            1.0, 0.0,
            1.0, 1.0,
            0.0, 1.0,

            # Back
            0.0, 1.0,
            0.0, 0.0,
            1.0, 0.0,
            1.0, 0.0,
            1.0, 1.0,
            0.0, 1.0,

            # Left
            0.0, 1.0,
            0.0, 0.0,
            1.0, 0.0,
            1.0, 0.0,
            1.0, 1.0,
            0.0, 1.0,

            # Right
            0.0, 1.0,
            0.0, 0.0,
            1.0, 0.0,
            1.0, 0.0,
            1.0, 1.0,
            0.0, 1.0,

            # Top
            0.0, 1.0,
            0.0, 0.0,
            1.0, 0.0,
            1.0, 0.0,
            1.0, 1.0,
            0.0, 1.0,

            # Bottom
            0.0, 1.0,
            0.0, 0.0,
            1.0, 0.0,
            1.0, 0.0,
            1.0, 1.0,
            0.0, 1.0,
        ],
        normals=[
            # Front
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,
            0.0, 0.0, 1.0,

            # Back
            0.0, 0.0, -1.0,
            0.0, 0.0, -1.0,
            0.0, 0.0, -1.0,
            0.0, 0.0, -1.0,
            0.0, 0.0, -1.0,
            0.0, 0.0, -1.0,

            # Left
            1.0, 0.0, 0.0,
            1.0, 0.0, 0.0,
            1.0, 0.0, 0.0,
            1.0, 0.0, 0.0,
            1.0, 0.0, 0.0,
            1.0, 0.0, 0.0,

            # Right
            -1.0, 0.0, 0.0,
            -1.0, 0.0, 0.0,
            -1.0, 0.0, 0.0,
            -1.0, 0.0, 0.0,
            -1.0, 0.0, 0.0,
            -1.0, 0.0, 0.0,

            # Top
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 1.0, 0.0,

            # Bottom
            0.0, -1.0, 0.0,
            0.0, -1.0, 0.0,
            0.0, -1.0, 0.0,
            0.0, -1.0, 0.0,
            0.0, -1.0, 0.0,
            0.0, -1.0, 0.0,
        ]
    )
