from typing import Union, Callable
from core.world import World
from core.engine import Engine
from server.socket_transmitter import SocketTransmitter
from server.server_transporter import ServerTransporter


class ServerEngine(Engine):
    def __init__(self, world: World, ip: str, port: int):
        super(ServerEngine, self).__init__(world)
        self.transmitter = SocketTransmitter(ip, port)
        self.transporter = ServerTransporter(self.transmitter)
        self.transporter.event_emitter.on('request', self.handle_request)

    def get_clients(self):
        return self.transmitter.clients

    def handle_request(self, request: Union[dict, str], response: Callable):
        if request['request']['command'] == 'get_state':
            response(self.world.get_state())
            return True

    def tick(self):
        super(ServerEngine, self).tick()

        self.transporter.run()

    def shutdown(self):
        self.transmitter.close()
