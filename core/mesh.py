from core.engine import Engine
import pythree


class Mesh:
    def __init__(self, geometry: pythree.Geometry, engine: Engine):
        self.geometry = geometry

        self.vertex_buffer = None
        self.normal_buffer = None
        self.uv_buffer = None

        engine.register_mesh(self)

    def set_vertex_buffer(self, buffer):
        self.vertex_buffer = buffer

    def set_normal_buffer(self, buffer):
        self.normal_buffer = buffer

    def set_uv_buffer(self, buffer):
        self.uv_buffer = buffer

    def get_vertex_buffer(self):
        return self.vertex_buffer

    def get_normal_buffer(self):
        return self.normal_buffer

    def get_uv_buffer(self):
        return self.uv_buffer
