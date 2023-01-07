from core.map_object import MapObject
from game.entities.star_ship import StarShip
from core.vector3 import Vector3


class Planet(MapObject):
    def __init__(self, radius: float,  weight: int, position: Vector3, class_name: str):
        super(Planet, self).__init__(position, class_name)
        self.weight = weight
        self.radius = radius

    def calculate_gravity(self, star_ship: StarShip):
        distance = self.position.calculate_distance(star_ship.position)

        # Newton's formula of universal gravitation
        # 6.67 * 10**-6 - gravitanional constant
        force = 6.67 * 10**-6 * self.weight * star_ship.weight / distance**2

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
