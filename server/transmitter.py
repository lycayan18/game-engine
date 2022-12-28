import socket
import json
from typing import Callable
from core.utils.event_emitter import EventEmitter


class Transmitter:
    def __init__(self, ip, port):
        self.event_emitter = EventEmitter()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))

    def on(self, callback: Callable):
        self.event_emitter.on('response', callback)

    def send_data(self, data: str):
        self.sock.send(data.encode('utf-8'))

    def get_data(self):
        try:
            data = json.loads(self.sock.recv(2 ** 32).decode('utf-8'))
            self.event_emitter.emit('response', data)
        except InterruptedError:
            print('Transmitter: the data recieving was interrupted')
        except Exception:
            print('Transmitter: Invalid data')

    def close(self):
        self.sock.close()
