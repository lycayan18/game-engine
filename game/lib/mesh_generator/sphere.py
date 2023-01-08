"""
GET OUT OF HERE!
YOU CANNOT BEAT CODE WRITTEN BY THE DEVIL ITSELF!
"""

import math
from pythree import Geometry
from core.vector3 import Vector3


def generate_sphere(radius: float, n_slices: int, n_stacks: int) -> Geometry:
    """
    Generates UV sphere.
    """

    # Generate points ( vertexes ) and normals/uvs for them

    vertexes: list[list[float]] = []
    vertex_uvs: list[list[float]] = []
    vertex_normals: list[list[float]] = []

    vertices: list[float] = []

    vertexes.append((0.0, 1.0, 0.0))
    vertex_normals.append((0.0, 1.0, 0.0))
    vertex_uvs.append((0.0, 0.0))

    for i in range(n_stacks - 1):
        # Some magic formulas and lines of code...
        phi = math.pi * (i + 1) / (n_stacks)

        for j in range(n_slices):
            theta = 2.0 * math.pi * j / n_slices

            x = math.sin(phi) * math.cos(theta) * radius
            y = math.cos(phi) * radius
            z = math.sin(phi) * math.sin(theta) * radius

            vertexes.append((x, y, z))
            vertex_normals.append((x, y, z))
            vertex_uvs.append((j / n_slices, (i + 1) / n_stacks))

    vertexes.append((0.0, -1.0, 0.0))
    vertex_normals.append((0.0, -1.0, 0.0))
    vertex_uvs.append((0.0, 1.0))

    normals: list[float] = []
    uvs: list[float] = []

    # *********************
    # * Generate triangles from vertexes
    # *********************

    # Add top/bottom triangles
    for i in range(0, n_slices + 1):
        # Another magic indexes

        i0 = i + 1
        i1 = (i + 1) % n_slices + 1
        i2 = (i + 1) % n_slices + n_slices * (n_stacks - 2) + 1
        i3 = i + n_slices * (n_stacks - 2) + 1

        vertices.extend((*vertexes[0], *vertexes[i0], *vertexes[i1]))
        vertices.extend((*vertexes[-1], *vertexes[i2], *vertexes[i3]))

        normals.extend(
            (*vertex_normals[0], *vertex_normals[i0], *vertex_normals[i1]))
        normals.extend(
            (*vertex_normals[-1], *vertex_normals[i2], *vertex_normals[i3]))

        # Magic line "(vertex_uvs[i1][0] + vertex_uvs[i0][0]) * 0.5" gives natural UV-sphere coordinates
        uvs.extend((*((vertex_uvs[i1][0] + vertex_uvs[i0][0]) * 0.5, 0.0),
                    *vertex_uvs[i0], *vertex_uvs[i1]))
        uvs.extend((*((vertex_uvs[i2][1] + vertex_uvs[i3][1]) * 0.5, 1.0),
                    *vertex_uvs[i2], *vertex_uvs[i3]))

    # Add other triangles
    for j in range(n_stacks - 2):
        j0 = j * n_slices + 1
        j1 = (j + 1) * n_slices + 1

        for i in range(n_slices):
            # More magic indexes!

            i0 = j0 + i
            i1 = j0 + (i + 1) % n_slices
            i2 = j1 + i
            i3 = j1 + (i + 1) % n_slices

            # Extend by two triangles at one call
            # Just splitting quad into two triangles
            vertices.extend((
                *vertexes[i2], *vertexes[i0], *vertexes[i1],
                *vertexes[i2], *vertexes[i3], *vertexes[i1],
            ))

            uvs.extend((
                *vertex_uvs[i2], *vertex_uvs[i0], *vertex_uvs[i1],
                *vertex_uvs[i2], *vertex_uvs[i3], *vertex_uvs[i1],
            ))

            normals.extend((
                *vertex_normals[i2], *vertex_normals[i0], *vertex_normals[i1],
                *vertex_normals[i2], *vertex_normals[i3], *vertex_normals[i1],
            ))

    return Geometry(vertices, uvs, normals)
