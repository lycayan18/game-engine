from core.entities.player import Player
from game.weapons.weapon import Weapon
from core.vector3 import Vector3
from game.lib.collision_detection.shapes.box import Box
from game.lib.rotation_to_direction import rotation_to_direction


class StarShip(Player):
    def __init__(self, weapon: Weapon, speed: int = 5/60, weight: int = 1000, rotation: Vector3 = None,
                 *args, **kwargs):
        super(StarShip, self).__init__(*args, **kwargs)
        self.weapon = weapon
        self.weapon.set_owner(self.id)

        self.speed = speed
        self.weight = weight
        self.rotation = rotation or Vector3(0, 0, 0)

        self.starship_bounding_box = Box(
            Vector3(1.214, 0.8, 2.0), self.get_position(), self.get_rotation())

    def get_collision_model(self) -> Box:
        return Box(Vector3(1.214, 0.8, 2.0), self.get_position(), self.get_rotation())

    def get_rotation(self) -> Vector3:
        return self.rotation

    def set_weapon(self, weapon: Weapon):
        self.weapon = weapon

    def move(self):
        direction = rotation_to_direction(self.rotation)
        self.position += direction * Vector3(self.speed * 0.0)

    def set_rotation(self, rotation: Vector3):
        self.rotation = rotation
        self.push_event({
            'type': 'set_rotation',
            'rotation': {
                'x': rotation.x,
                'y': rotation.y,
                'z': rotation.z
            }
        })

    def get_speed(self) -> float:
        return self.speed

    def set_speed(self, speed: float):
        self.speed = speed
        self.push_event({
            'type': 'set_speed',
            'speed': self.speed
        })

    def shoot_event(self, position: Vector3, rotation: Vector3, weapon_state: dict):
        """
        Shoots by weapon from provided position.
        Useful for events as this function provides convenient interface for emitting
        event with parameters it was originally called with.\n
        For shooting call "shoot" function, this function is for other purposes.
        """

        self.weapon.set_state(weapon_state)

        if self.weapon.shoot(current_position=position, rotation=rotation):
            self.push_event({
                "type": "weapon_shoot",
                "weapon_state": weapon_state,
                "position": {
                    "x": position.x,
                    "y": position.y,
                    "z": position.z
                },
                "rotation": {
                    "x": rotation.x,
                    "y": rotation.y,
                    "z": rotation.z
                }
            })

    def shoot(self):
        self.shoot_event(self.position, self.rotation, self.weapon.get_state())

    def think(self):
        self.move()

    def set_state(self, state: dict):
        super(StarShip, self).set_state(state)

        self.weapon.set_state(state.get("weapon"))

        self.rotation = Vector3(**state['rotation'])

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
            # To avoid enabling event registering when it was disabled
            currently_registering_events = self.register_events

            if currently_registering_events:
                # Stop registering events to avoid registering event that we're emitting now.
                # Otherwise it may break game logic as World expects that Entity won't register
                # events it's currently emitting
                self.stop_registering_events()

            if event.get("type", None) == "weapon_shoot":
                self.shoot_event(
                    Vector3(**event["position"]), Vector3(**event["rotation"]), event["weapon_state"])
            elif event.get("type", None) == "set_speed":
                self.set_speed(event["speed"])
            elif event.get("type", None) == "set_rotation":
                self.set_rotation(Vector3(**event["rotation"]))

            if currently_registering_events:
                self.start_registering_events()

        return super().emit_events(events)
