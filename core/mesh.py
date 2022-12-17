import pythree
from core.material import Material


class Mesh:
    def __init__(self, geometry: pythree.Geometry, material: Material):
        self.geometry = geometry
        self.material = material

