from typing import Union, Callable

from core.world import World
from core.registry import Registry
from server.server_engine import ServerEngine


class Server(ServerEngine):
    def __init__(self, ip: str, port: int):
        super(Server, self).__init__(World(Registry()), ip, port)

        self.last_events = []

        self.event_emitter.on("pull_events", self.handle_pull_events_request)
        self.event_emitter.on("push_events", self.handle_push_events_request)
        self.event_emitter.on("shoot", self.handle_shoot_events_request)

    def handle_request(self, request: Union[dict[str, dict], dict, str], response: Callable):
        # проверка на обработку запроса ServerEngine'ом
        if super(Server, self).handle_request(request, response):
            return

        self.event_emitter.emit(request["request"]["command"], response, **request["request"]["parameters"])

        if request['request']['command'] == 'shoot':
            self.world.get_entity_by_id(
                request['request']['entity_id']).shoot()

        if request['request']['command'] == "pull_events":
            response(self.last_events[:])

        if request['request']['command'] == 'push_events':
            self.world.emit_events(request['request']['params'])

    def handle_pull_events_request(self, response, **params):
        pass

    def handle_push_events_request(self, response, **params):
        pass

    def handle_shoot_events_request(self, response, **params):
        pass

    def tick(self):
        super().tick()

        self.last_events = self.world.get_last_events()
