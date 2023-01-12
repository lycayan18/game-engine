from core.entity import Entity
from core.vector3 import Vector3


class HealthyEntity(Entity):
    def __init__(self, position: Vector3, class_name: str, health: float = 100.0):
        super().__init__(position, class_name)
        self.health = health
        self.alive = True

    def dead(self):
        self.alive = False
        self.health = -1

    def heal(self, amount_health: float):
        self.health += amount_health

    def damage(self, amount_damage: float):
        self.health -= amount_damage
        if self.health <= 0:
            self.dead()

    def set_state(self, state: dict):
        super(HealthyEntity, self).set_state(state)
        self.health = state.get('health', 0)

    def get_state(self) -> dict:
        state = {
            **super(HealthyEntity, self).get_state(),
            'health': self.health
        }

        return state

    @staticmethod
    def from_state(state: dict):
        ent = HealthyEntity(Vector3(0, 0, 0), "", 100.0)

        ent.set_state(state)

        return ent
