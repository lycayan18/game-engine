import pygame
from client.base_material import BaseMaterial
from client.client_entity import ClientEntity
from client.sound_modules.pygame.sound import PygameSound
from core.mesh import Mesh
from core.vector3 import Vector3
from client.entities.sound_entity import SoundEntity
from game.entities.star_ship import StarShip
from game.client.weapons.client_weapon import ClientWeapon
from game.client.weapons.laser_gun import ClientLaserGun
from game.client.app_state import AppState
from game.client.assets.assets import Assets


class ClientStarShip(ClientEntity):
    mesh = None
    material = None

    def __init__(self, position: Vector3, weapon: ClientWeapon, class_name: str, material: BaseMaterial,
                 mesh: Mesh = None,
                 rotation: Vector3 = None, scale: Vector3 = None):

        rotation = rotation or Vector3(0, 0, 0)
        scale = scale or Vector3(1, 1, 1)

        super(ClientStarShip, self).__init__(
            StarShip(weapon=weapon, speed=300, weight=1000, rotation=rotation, class_name=class_name, position=position,
                     health=100.0),
            class_name, material, mesh, rotation, scale
        )

        self.sound_entity: SoundEntity = SoundEntity(
            PygameSound(pygame.mixer.Sound(
                "./game/client/assets/sounds/space_engine.wav"
            )), self.position, "entity_sfx", True, 40)

        self.sound_entity.id = -1

        AppState.world.add_entity(self.sound_entity, False)

        self.sound_entity.sound.set_repeatable(True)

        self.sound_entity.play()

        self.weapon = weapon

    def get_health(self):
        return self.entity.health

    def dead_animation(self):
        self.push_event({
            "type": "play_dead_animation"
        })

    def shutoff_engine_sound(self):
        self.sound_entity.stop()
        self.sound_entity.sound.set_repeatable(False)

    def dead(self):
        self.entity.dead()
        self.dead_animation()

    def shoot(self):
        self.entity.shoot()

    def get_speed(self):
        return self.entity.get_speed()

    def set_speed(self, speed: float):
        self.entity.set_speed(speed)

    def get_rotation(self):
        return self.entity.get_rotation()

    def set_rotation(self, rotation: Vector3):
        self.rotation = rotation

        self.entity.set_rotation(rotation)

    def emit_events(self, events: list[dict]):
        self.entity.emit_events(events)

        for event in events:
            # To avoid enabling event registering when it was disabled
            currently_registering_events = self.register_events

            if currently_registering_events:
                self.stop_registering_events()

            if event.get("type", None) == "play_dead_animation":
                self.dead_animation()

            if currently_registering_events:
                self.start_registering_events()

        super().emit_events(events)

        self.rotation = self.entity.rotation

    # These are just wrappers as this class is a StarShip entity wrapper

    def get_state(self) -> dict:
        return self.entity.get_state()

    def set_state(self, state: dict):
        self.entity.set_state(state)

        # Update link to position
        self.position = self.entity.position

        self.entity.rotation = self.rotation
        self.weapon.set_owner(self.id)

    def get_last_events(self) -> list[dict]:
        return self.entity.get_last_events()

    def emit_events(self, events: list[dict]):
        self.entity.emit_events(events)

    def think(self):
        self.sound_entity.position = self.position

    @staticmethod
    def from_state(state: dict):
        weapon = ClientLaserGun.from_state(
            state["weapon"], AppState.get_world())

        entity = ClientStarShip(Vector3(0, 0, 0), weapon,
                                state['class_name'], ClientStarShip.material, ClientStarShip.mesh)

        entity.id = state["id"]
        entity.weapon.set_owner(entity.id)

        entity.set_state(state)

        # Set initial rotation
        entity.rotation.x = state["rotation"]["x"]
        entity.rotation.y = state["rotation"]["y"]
        entity.rotation.z = state["rotation"]["z"]

        return entity
