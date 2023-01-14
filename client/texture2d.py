from PIL import Image
from core.utils.event_emitter import EventEmitter
from client.client_engine import ClientEngine


class Texture2D:
    def __init__(self, width: int, height: int, engine: ClientEngine):
        self.width = width
        self.height = height
        self.data = None

        self.registered = False
        self.engine = engine
        self.event_emitter = EventEmitter()

    def register(self):
        if not self.registered:
            self.registered = True
            self.engine.register_texture(self)

    def get_size(self):
        return self.width, self.height

    def get_data(self):
        return self.data

    def update(self):
        """
        Emits update event. Useful when updating texture data to mark renderers that they can update
        texture data.
        """
        self.event_emitter.emit("update", self)

    def load_from_data(self, data):
        self.data = data

        self.register()

        # For convenient interface like "TexturedMaterial(Texture2D(...).load_from_data(...))"
        return self

    def load_from_file(self, path: str):
        im = Image.open(path)

        self.width = im.width
        self.height = im.height

        data = im.convert("RGBA").tobytes()

        im.close()

        return self.load_from_data(data)
