from core.entities.player import Player
from game.entities.weapon import Weapon


class StarShip(Player):
    def __init__(self, weapon: Weapon, weight=1000, *args, **kwargs):
        super(StarShip, self).__init__(*args, **kwargs)
        self.weapon = weapon
        self.weight = weight

    def set_weapon(self, weapon):
        self.weapon = weapon

    def shoot(self):
        self.weapon.shoot(current_position=self.position)

    def set_state(self, state: dict):
        super(StarShip, self).set_state(state)
        self.health = state.get('weapon', None)

    def get_state(self) -> dict:
        state = {
            **super(StarShip, self).get_state(),
            'weapon': self.health
        }

        return state
