import socket
from typing import Callable
from core.utils.event_emitter import EventEmitter


class SocketTransmitter:
    def __init__(self, ip, port):
        self.event_emitter = EventEmitter()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((ip, port))
        self.sock.settimeout(0.00)
        self.sock.listen(5)

        self.clients: list[socket.socket] = []

    def accept_client(self):
        try:
            client, address = self.sock.accept()
            self.clients.append(client)
        except BlockingIOError:
            pass
        except socket.timeout:
            pass
        except InterruptedError:
            print('SocketTransmitter: the client acception was interrupted')

    def get_request(self):
        for client in self.clients:
            data = ''

            try:
                while True:
                    try:
                        data += client.recv(4096).decode('utf-8')
                    except socket.timeout:
                        if data and data[-1] != '/':
                            continue
                        else:
                            break
            except BlockingIOError:
                pass
            except ConnectionResetError:
                self.clients.remove(client)

            data = data.strip()

            if data:
                for req in data[:-1].split('/'):
                    self.event_emitter.emit('request', req,
                                            lambda res: self.send_data(client, res))

    def on(self, data: str, callback: Callable):
        self.event_emitter.on(data, callback)

    def run(self):
        self.accept_client()
        self.get_request()

    def close(self):
        self.sock.close()

    @staticmethod
    def send_data(connection: socket.socket, data: str):
        # we receive the client's data (connection)
        # and send a response based on this data
        # To send all data through sockets, without sockets to wait until buffer fills up
        to_send = data + ' ' * (4096 - (len(data) + 1) % 4096) + '/'

        connection.send(to_send.encode('utf-8'))
