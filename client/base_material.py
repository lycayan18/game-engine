from client.client_engine import ClientEngine


class BaseMaterial:
    def __init__(self, engine: ClientEngine, name: str, vertex_source: str, fragment_source: str):
        self.engine = engine
        self.name = name
        self.vertex_source = vertex_source
        self.fragment_source = fragment_source

        self.engine.register_material(self)

    def get_vertex_source(self):
        return self.vertex_source

    def get_fragment_source(self):
        return self.fragment_source

    def get_name(self):
        return self.name

    def get_uniforms(self) -> list[dict]:
        """
        Return uniforms values in format:\n
        {\n
            "name": <uniform name>,\n
            "value": <value>,\n
            "type": "f[1 | 2 | 3 | 4][v]" | "i[1 | 2 | 3 | 4][v]" | "mat[2 | 3 | 4]" | "texture2D"\n
        }
        """

        return []
