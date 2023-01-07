import json
from server.socket_transmitter import SocketTransmitter
from core.utils.event_emitter import EventEmitter


class ServerTransporter:
    def __init__(self, transmitter: SocketTransmitter):
        self.transmitter = transmitter
        self.event_emitter = EventEmitter()
        self.transmitter.on('request', self.handle_request)

    def send_data(self, data_id: str, response: dict | str, send_response):
        data = {
            'id': data_id,
            'out': response
        }
        response = json.dumps(data)
        send_response(response)

    def handle_request(self, request: str, send_response):
        data = json.loads(request)
        self.event_emitter.emit('request', data, lambda res: self.send_data(data['id'], res, send_response))

    def run(self):
        self.transmitter.run()
