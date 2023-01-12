from core.module import BaseModule
from client.camera import Camera


class GraphicsModule(BaseModule):
    def __init__(self, camera: Camera):
        super(GraphicsModule, self).__init__()
        self.camera = camera

    def get_camera(self) -> Camera:
        return self.camera

    def set_camera(self, camera: Camera):
        self.camera = camera
