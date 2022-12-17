from core.entities.healthy_entity import HealthyEntity


class Player(HealthyEntity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_state(self, state: dict):
        super(Player, self).set_state(state)

    def get_state(self):
        return super(Player, self).get_state()
