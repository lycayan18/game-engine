from client.client_engine import ClientEngine

from core.world import World


class Client(ClientEngine):
    def __init__(self, world: World, ip: str, port: int):
        super(Client, self).__init__(world, ip, port)

    def shoot(self, entity_id):
        request = {
            'entity_id': entity_id,
            'command': 'shoot'}
        self.send_data(request)

    def position_x(self, entity_id, coord):
        request = {
            'entity_id': entity_id,
            'position_x': coord}
        self.send_data(request)

    def position_y(self, entity_id, coord):
        request = {
            'entity_id': entity_id,
            'position_y': coord}
        self.send_data(request)

    def position_z(self, entity_id, coord):
        request = {
            'entity_id': entity_id,
            'position_z': coord}
        self.send_data(request)

    def rotation_x(self, entity_id, coord):
        request = {
            'entity_id': entity_id,
            'rotation_x': coord}
        self.send_data(request)

    def rotation_y(self, entity_id, coord):
        request = {
            'entity_id': entity_id,
            'rotation_y': coord}
        self.send_data(request)

    def rotation_z(self, entity_id, coord):
        request = {
            'entity_id': entity_id,
            'rotation_z': coord}
        self.send_data(request)

