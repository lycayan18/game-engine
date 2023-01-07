from typing import Union
from core.world import World
from core.engine import Engine
from client.transmitter import Transmitter
from client.transporter import Transporter
from client.graphics_module import GraphicsModule


class ClientEngine(Engine):
    def __init__(self, world: World, ip: str = None, port: int = None):
        super(ClientEngine, self).__init__(world)

        if ip is not None and port is not None:
            self.transmitter = Transmitter(ip, port)
            self.transporter = Transporter(self.transmitter)

    def register_material(self, material):
        """
        Reports to all modules about new registered material.
        Useful for abstracting out from what these modules are and reporting regardless
        of their purposes.
        """

        self.event_emitter.emit("material_registered", material)

    def handle_response(self, data: dict):
        self.world.set_state(data)

    def send_data(self, data: Union[dict, str]):
        self.transporter.send(data, self.handle_response)
