from client.base_material import BaseMaterial
from client.client_map_object import ClientMapObject
from core.mesh import Mesh
from core.vector3 import Vector3
from game.entities.planet import Planet
from game.entities.star_ship import StarShip


class ClientPlanet(ClientMapObject):
    def __init__(self, planet: Planet, material: BaseMaterial, mesh: Mesh = None, scale: Vector3 = None):
        super(ClientPlanet, self).__init__(map_object=planet, class_name=planet.class_name, material=material,
                                           mesh=mesh, scale=scale)

    def get_collision_model(self):
        self.map_object.get_collision_model()

    def calculate_gravity(self, star_ship: StarShip):
        self.map_object.calculate_gravity(star_ship)

    def set_state(self, state: dict):
        self.map_object.set_state(state)

    def get_state(self) -> dict:
        self.map_object.get_state()

    def think(self):
        self.map_object.get_state()

    @staticmethod
    def from_state(state: dict, material: BaseMaterial = None, mesh: Mesh = None):
        planet = Planet.from_state(state)
        return ClientPlanet(planet, material, mesh)
