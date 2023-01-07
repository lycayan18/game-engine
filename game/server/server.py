from typing import Union, Callable

from core.world import World
from core.registry import Registry
from server.server_engine import ServerEngine


class Server(ServerEngine):
    def __init__(self, ip: str, port: int):
        super(Server, self).__init__(World(Registry()), ip, port)

    def handle_request(self, request: Union[dict[str, dict], dict, str], response: Callable):
        # проверка на обработку запроса ServerEngine'ом
        if super(Server, self).handle_request(request, response):
            return

        if request['request']['command'] == 'shoot':
            self.world.get_entity_by_id(request['request']['entity_id']).shoot()

        if 'position_x' in request['request']:
            self.world.get_entity_by_id(request['request']['entity_id']).position.x = request['request']['position_x']

        if 'position_y' in request['request']:
            self.world.get_entity_by_id(request['request']['entity_id']).position.x = request['request']['position_y']

        if 'position_z' in request['request']:
            self.world.get_entity_by_id(request['request']['entity_id']).position.x = request['request']['position_z']

        if 'rotation_x' in request['request']:
            self.world.get_entity_by_id(request['request']['entity_id']).rotation.x = request['request']['rotation_x']

        if 'rotation_y' in request['request']:
            self.world.get_entity_by_id(request['request']['entity_id']).rotation.y = request['request']['rotation_y']

        if 'rotation_z' in request['request']:
            self.world.get_entity_by_id(request['request']['entity_id']).rotation.z = request['request']['rotation_z']




