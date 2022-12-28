import json
from core.world import World
from core.engine import Engine
from socket_transmitter import SocketTransmitter


class ServerEngine(Engine):
    def __init__(self, world: World, ip: str, port: int):
        super(ServerEngine, self).__init__(world)
        self.transmitter = SocketTransmitter(ip, port)
        self.transmitter.event_emitter.on('request', self.handle_request)

    def handle_request(self, request: str, send_data):
        data = json.loads(request)
        if data['request'] == 'get_state':
            send_data(self.generate_state_response(data['id']))

    def generate_state_response(self, data_id: int):
        state = self.world.get_state()
        data = {
            'id': data_id,
            'out': state
        }
        dump_data = json.dumps(data)
        return dump_data

    def tick(self):
        self.transmitter.run()
