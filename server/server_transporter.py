import json
from server.socket_transmitter import SocketTransmitter


class ServerTransporter:
    def __init__(self, transmitter: SocketTransmitter, world):
        self.transmitter = transmitter
        self.world = world
        self.transmitter.on('request', self.handle_request)

    def send_data(self, data_id: str, send_state):
        state = self.world.get_state()
        data = {
            'id': data_id,
            'out': state
        }
        response = json.dumps(data)
        send_state(response)

    def handle_request(self, request: str, send_state):
        data = json.loads(request)
        if data['request'] == 'get_state':
            self.send_data(data['id'], send_state)
