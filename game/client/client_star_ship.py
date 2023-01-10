from client.base_material import BaseMaterial
from client.client_entity import ClientEntity
from core.mesh import Mesh
from core.vector3 import Vector3
from game.entities.star_ship import StarShip
from game.entities.weapon import Weapon
from game.app_state import AppState


class ClientStarShip(ClientEntity):
    mesh = None
    material = None

    def __init__(self, position: Vector3, weapon: Weapon, class_name: str, material: BaseMaterial, mesh: Mesh = None,
                 rotation: Vector3 = None, scale: Vector3 = None):

        rotation = rotation or Vector3(0, 0, 0)
        scale = scale or Vector3(1, 1, 1)

        super(ClientStarShip, self).__init__(
            StarShip(weapon, 1000, rotation, class_name, position, 100.0),
            class_name, material, mesh, rotation, scale
        )

    def play_shoot_sound(self):
        self.push_event({
            "type": "shoot_sound"
        })

    def dead_animation(self):
        self.push_event({
            "type": "play_dead_animation"
        })

    def dead(self):
        self.entity.dead()
        self.dead_animation()

    def shoot(self):
        self.entity.shoot()
        self.play_shoot_sound()

    def emit_events(self, events: list[dict]):
        self.entity.emit_events(events)

        for event in events:
            # To avoid enabling event registering when it was disabled
            currently_registering_events = self.register_events

            if currently_registering_events:
                self.stop_registering_events()

            if event.get("type", None) == "play_dead_animation":
                self.dead_animation()
            elif event.get("type", None) == "shoot_sound":
                self.play_shoot_sound()

            if currently_registering_events:
                self.start_registering_events()

        return super().emit_events(events)

    # These are just wrappers as this class is a StarShip entity wrapper

    def get_state(self) -> dict:
        return self.entity.get_state()

    def set_state(self, state: dict):
        self.entity.set_state(state)

        # Update link to position
        self.position = self.entity.position

    @staticmethod
    def from_state(state: dict):
        weapon = Weapon.from_state(state["weapon"], AppState.get_world())

        entity = ClientStarShip(Vector3(0, 0, 0), weapon,
                                state['class_name'], ClientStarShip.material, ClientStarShip.mesh)

        entity.set_state(state)

        return entity
