from client.graphics_module import GraphicsModule
from client.transporter import Transporter
from client.transmitter import Transmitter
from core.engine import Engine
from core.world import World
from typing import Union, Callable
from typing import Any, Callable, Union


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

    def send_world_state_request(self):
        self.send_command("get_state", {}, self.world.set_state)

    def send_pull_events_request(self):
        self.send_command("pull_events", {}, self.world.emit_events)

    def send_events(self):
        self.send_command("push_events",
                          {"events": self.world.get_last_events()},
                          None, False)

    def send_command(self, command: str, parameters: dict, callback: Callable[[Any], None], need_response: bool = True):
        self.transporter.send({
            "command": command,
            "parameters": parameters
        }, callback, need_response)

    def tick(self):
        super(ClientEngine, self).tick()

        self.transporter.run()

    def shutdown(self):
        self.transmitter.close()
