from typing import Union, Callable

from datetime import datetime

from core.world import World
from core.registry import Registry
from game.entities.star_ship import StarShip
from server.server_engine import ServerEngine
from game.generate_planet import generate_planet
from game.generate_star_ship import generate_star_ship


class Server(ServerEngine):
    def __init__(self, registry: Registry, ip: str, port: int):
        super(Server, self).__init__(World(registry), ip, port)

        generate_planet(self.world, 5)

        self.last_events = []

        self.event_emitter.on("pull_events", self.handle_pull_events_request)
        self.event_emitter.on("push_events", self.handle_push_events_request)
        self.event_emitter.on(
            "get_client_id", self.handle_get_client_id_request)
        self.event_emitter.on("get_current_entity_id",
                              self.handle_get_current_entity_id_request)

        self.event_emitter.on("respawn", self.handle_respawn_request)

        self.client_unique_id = 0

        self.clients_with_id: dict[int, StarShip] = {}

    def handle_request(self, request: Union[dict[str, dict], dict, str], response: Callable):
        # проверка на обработку запроса ServerEngine'ом
        if super(Server, self).handle_request(request, response):
            return

        self.event_emitter.emit(
            request["request"]["command"], response, request["request"]["parameters"])

    def handle_respawn_request(self, response: Callable, parameters: dict):
        star_ship = generate_star_ship(
            self.world, self.clients_with_id[parameters['client_id']].id)

        self.world.remove_entity(self.clients_with_id[parameters['client_id']])

        self.clients_with_id[parameters['client_id']] = star_ship
        self.world.add_entity(star_ship, False)

    def handle_get_current_entity_id_request(self, response: Callable, parameters: dict):
        response(self.clients_with_id[parameters['client_id']].id)

    def handle_get_client_id_request(self, response: Callable, parameters: dict):
        star_ship = generate_star_ship(self.world)
        self.world.add_entity(star_ship)

        self.clients_with_id[self.client_unique_id] = star_ship
        self.client_unique_id += 1

        response(self.client_unique_id - 1)

    def handle_pull_events_request(self, response: Callable, parameters: dict):
        response(self.last_events[:])

    def handle_push_events_request(self, response: Callable, parameters):
        self.world.emit_events(parameters['events'])

    def tick(self):
        super(Server, self).tick()

        self.last_events = self.world.get_last_events()
