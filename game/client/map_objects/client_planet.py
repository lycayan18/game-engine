from core.vector3 import Vector3
from core.mesh import Mesh
from client.base_material import BaseMaterial
from client.materials.diffuse import DiffuseMaterial
from client.client_map_object import ClientMapObject
from game.entities.planet import Planet
from game.entities.star_ship import StarShip
from game.lib.mesh_generator.sphere import generate_sphere
from game.client.app_state import AppState


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
    def from_state(state: dict):
        material = DiffuseMaterial(AppState.get_engine(), Vector3(
            0.0, -1.0, 0.0), [0.33, 0.08, 1.0])

        planet = Planet.from_state(state, AppState.get_world())

        obj = ClientPlanet(planet, material, Mesh(
            generate_sphere(planet.radius, 32, 16), AppState.get_engine()))

        obj.id = planet.id

        return obj
