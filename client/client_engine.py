from typing import Union, Callable
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

    def register_texture(self, texture):
        """
        Reports to all modules about new registered texture.
        Useful for abstracting out from what these modules are and reporting regardless
        of their purposes.
        """

        self.event_emitter.emit("texture_registered", texture)

    def handle_response(self, data: dict):
        self.world.set_state(data)

    def send_command(self, command: str, parameters: dict, callback: Callable[[Union[dict, str]], None]):
        self.transporter.send({
            "command": command,
            "parameters": parameters
        }, callback)
