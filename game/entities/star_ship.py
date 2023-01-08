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

    def shoot_event(self, position: Vector3):
        """
        Shoots by weapon from provided position.
        Useful for events as this function provides convenient interface for emitting
        event with parameters it was originally called with.\n
        For shooting call "shoot" function, this function is for other purposes.
        """

        self.push_event({
            "type": "weapon_shoot",
            "position": {
                "x": position.x,
                "y": position.y,
                "z": position.z
            }
        })

        self.weapon.shoot(current_position=position)

    def shoot(self):
        self.shoot_event(self.position)

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

    def emit_events(self, events: list[dict]):
        for event in events:
            if event.get("type", None) == "weapon_shoot":
                # To avoid enabling event registering when it was disabled
                currently_registering_events = self.register_events

                if currently_registering_events:
                    # Stop registering events to avoid registering event that we're emitting now.
                    # Otherwise it may break game logic as World expects that Entity won't register
                    # events it's currently emitting
                    self.stop_registering_events()

                self.shoot_event(Vector3(**event["position"]))

                if currently_registering_events:
                    self.start_registering_events()

        return super().emit_events(events)
