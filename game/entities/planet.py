from core.map_object import MapObject
from core.world import World
from game.entities.star_ship import StarShip
from core.vector3 import Vector3
from game.lib.collision_detection.shapes.sphere import Sphere


class Planet(MapObject):
    def __init__(self, world: World, radius: float, weight: int, position: Vector3, class_name: str):
        super(Planet, self).__init__(position, class_name)
        self.world = world
        self.weight = weight
        self.radius = radius

        self.sphere = Sphere(self.radius, self.position)

    def get_collision_model(self) -> Sphere:
        return self.sphere

    def calculate_gravity(self, star_ship: StarShip):
        distance = self.position.calculate_distance(star_ship.position)

        # Newton's formula of universal gravitation
        # 6.67 * 10**-6 - gravitational constant
        force = 6.67 * 10**-8 * self.weight * star_ship.weight / distance ** 2

        return force

    def set_state(self, state: dict):
        super(Planet, self).set_state(state)
        self.weight = state.get('weight', 0)
        self.radius = state.get('radius', 0)

    def get_state(self) -> dict:
        state = {
            **super(Planet, self).get_state(),
            'weight': self.weight,
            'radius': self.radius
        }

        return state

    def think(self):
        for entity in self.world.entities:
            if isinstance(entity, StarShip):
                force = self.calculate_gravity(entity)

                entity.acceleration += Vector3.normalized(
                    self.position - entity.position) * Vector3(force)

                if self.sphere.collide_point(entity.get_position()):
                    entity.dead()

    @staticmethod
    def from_state(state: dict, world: World = None):
        planet = Planet(world, 0.0, 0.0, None, "")

        planet.set_state(state)

        return planet
