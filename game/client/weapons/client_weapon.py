from core.world import World
from game.weapons.weapon import Weapon
from client.sound import Sound


class ClientWeapon:
    """
    Class-wrapper, the only function of is to play shooting sound when calling
    "shoot" method.
    """

    def __init__(self, weapon: Weapon, shoot_sound: Sound = None):
        self.weapon = weapon
        self.shoot_sound = shoot_sound

    def shoot(self, *args, **kwargs):
        if self.shoot_sound:
            self.shoot_sound.play()

        # We don't need to call super.shoot as we don't want bullet to be spawned.
        # It spawns in server world and then we get it through world state.

    def set_bullet_count(self, count: int):
        self.weapon.set_bullet_count(count)

    def is_reloaded(self) -> bool:
        return self.weapon.is_reloaded()

    def recharge(self):
        self.weapon.recharge()

    def get_state(self) -> dict:
        return self.weapon.get_state()

    def set_state(self, state: dict) -> dict:
        self.weapon.set_state(state)

    @staticmethod
    def from_state(state: dict, world: World, shoot_sound: Sound = None):
        return ClientWeapon(Weapon.from_state(state, world), shoot_sound)
