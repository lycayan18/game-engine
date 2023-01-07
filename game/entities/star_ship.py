from core.entities.player import Player
from game.entities.weapon import Weapon
from core.vector3 import Vector3


class StarShip(Player):
    def __init__(self, weapon: Weapon, weight=1000, rotation: Vector3 = None, *args, **kwargs):
        super(StarShip, self).__init__(*args, **kwargs)
        self.weapon = weapon
        self.weight = weight
        self.rotation = rotation or Vector3(0, 0, 0)

    def set_weapon(self, weapon: Weapon):
        self.weapon = weapon

    def shoot(self):
        self.weapon.shoot(current_position=self.position)

    def set_state(self, state: dict):
        super(StarShip, self).set_state(state)
        self.weapon = state.get('weapon', None)
        self.rotation = Vector3(
            state['rotation']['x'], state['rotation']['y'], state['rotation']['z'])

    def get_state(self) -> dict:
        state = {
            **super(StarShip, self).get_state(),
            'weapon': self.weapon.get_state(),
            'rotation': {
                'x': self.rotation.x,
                'y': self.rotation.y,
                'z': self.rotation.z
            }
        }

        return state
