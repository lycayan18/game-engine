from core.engine import Engine
import pythree


class Mesh:
    def __init__(self, geometry: pythree.Geometry, engine: Engine):
        self.geometry = geometry

        engine.register_mesh(self)
