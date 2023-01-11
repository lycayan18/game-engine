from game.client.entities.client_bullet import ClientBullet
from game.entities.bullet import Bullet


class LaserBullet(ClientBullet):
    material = None,
    mesh = None

    @staticmethod
    def from_state(state: dict):
        bullet = Bullet.from_state(state)
        return ClientBullet(bullet, LaserBullet.material, LaserBullet.mesh)