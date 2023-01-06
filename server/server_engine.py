from core.world import World
from core.engine import Engine
from server.socket_transmitter import SocketTransmitter
from server.server_transporter import ServerTransporter


class ServerEngine(Engine):
    def __init__(self, world: World, ip: str, port: int):
        super(ServerEngine, self).__init__(world)
        self.transmitter = SocketTransmitter(ip, port)
        self.transporter = ServerTransporter(self.transmitter, self.world)

    def tick(self):
        self.transmitter.run()
