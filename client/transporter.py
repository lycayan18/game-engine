import json
from client.transmitter import Transmitter
from typing import Callable, Union


class Transporter:
    def __init__(self, transmitter: Transmitter):
        self.id_count = 0
        self.transmitter = transmitter
        self.transmitter.on('response', self.handle_server_response)
        self.callbacks = {}

    def send(self, data: Union[dict, str], callback: Callable):
        request = {
            'id': self.id_count,
            'request': data
        }

        self.transmitter.send_data(json.dumps(request))
        self.callbacks[self.id_count] = callback
        self.id_count += 1

    def handle_server_response(self, response_data: str):
        data = json.loads(response_data)
        self.callbacks[data['id']](data['out'])

        self.callbacks[data['id']] = None

    def run(self):
        self.transmitter.run()
