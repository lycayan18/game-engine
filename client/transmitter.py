import socket
from typing import Callable
from core.utils.event_emitter import EventEmitter


class Transmitter:
    def __init__(self, ip, port):
        self.event_emitter = EventEmitter()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))

        self.sock.settimeout(0.01)

    def on(self, data: str,  callback: Callable):
        self.event_emitter.on(data, callback)

    def send_data(self, data: str):
        # To send all data through sockets, without sockets to wait until buffer fills up
        to_send = data + ' ' * (4096 - (len(data) + 1) % 4096) + '/'

        self.sock.send(to_send.encode('utf-8'))

    def get_data(self):
        try:
            data = ''

            while True:
                try:
                    # Get all data packet by packet
                    data += self.sock.recv(4096).decode('utf-8')
                except socket.timeout:
                    if data and data[-1] != '/':
                        continue
                    else:
                        break

            if data:
                for res in data[:-1].split('/'):
                    self.event_emitter.emit('response', res.strip())
        except InterruptedError:
            print('Transmitter: the data receiving was interrupted')
        except RecursionError as e:
            raise e
        except Exception as e:
            print('Transmitter: an error has occurred:', e)
            raise e

    def run(self):
        self.get_data()

    def close(self):
        self.sock.close()
