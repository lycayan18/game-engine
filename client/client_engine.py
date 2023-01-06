from typing import Union
from core.world import World
from core.engine import Engine
from client.transmitter import Transmitter
from client.transporter import Transporter


class ClientEngine(Engine):
    def __init__(self, world: World, ip: str, port: int):
        super(ClientEngine, self).__init__(world)
        self.transmitter = Transmitter(ip, port)
        self.transporter = Transporter(self.transmitter)

    def handle_response(self, data: dict):
        self.world.set_state(data)

    def send_data(self, data: Union[dict, str]):
        self.transporter.send(data, self.handle_response)