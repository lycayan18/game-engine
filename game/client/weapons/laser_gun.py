from core.world import World
from game.weapons.laser_gun import LaserGun
from game.client.weapons.client_weapon import ClientWeapon
from game.client.app_state import AppState
from game.client.assets.assets import Assets


class ClientLaserGun(ClientWeapon):
    def __init__(self):
        super(ClientLaserGun, self).__init__(
            weapon=LaserGun(AppState.world),
            shoot_sound=Assets.sounds.laser_gun_shot
        )

    @staticmethod
    def from_state(state: dict, world: World):
        return ClientWeapon(LaserGun.from_state(state, world), Assets.sounds.laser_gun_shot)
