import socket
from typing import Callable
from core.utils.event_emitter import EventEmitter


class SocketTransmitter:
    def __init__(self, ip, port):
        self.event_emitter = EventEmitter()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((ip, port))
        self.sock.setblocking(False)
        self.sock.listen(5)

        self.clients = []

    def accept_client(self):
        try:
            client, address = self.sock.accept()
            client.setblocking(False)
            self.clients.append(client)
        except BlockingIOError:
            pass

    def get_request(self):
        for client in self.clients:
            try:
                self.event_emitter.emit('request', client.recv(2 ** 32).decode('utf-8'),
                                        lambda data: self.send_data(client, data))
            except BlockingIOError:
                self.clients.remove(client)

    def on(self, data: str, callback: Callable):
        self.event_emitter.on(data, callback)

    def run(self):
        self.accept_client()
        self.get_request()

    @staticmethod
    def send_data(connection: socket.socket, data: str):
        # we receive the client's data (connection)
        # and send a response based on this data
        connection = connection
        connection.send(data.encode('utf-8'))
