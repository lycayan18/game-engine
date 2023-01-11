from client.base_material import BaseMaterial
from client.client_entity import ClientEntity
from core.mesh import Mesh
from core.vector3 import Vector3
from game.entities.bullet import Bullet
from game.entities.star_ship import StarShip


class ClientBullet(ClientEntity):
    def __init__(self, bullet: Bullet, material: BaseMaterial, mesh: Mesh = None, scale: Vector3 = None):
        super(ClientBullet, self).__init__(bullet, bullet.class_name, material, mesh, bullet.rotation, scale)
        self.bullet = bullet

    def calculate_distance(self):
        self.bullet.calculate_distance()

    def move(self):
        self.bullet.move()

    def collision_check(self, star_ship: StarShip):
        self.bullet.collision_check(star_ship)

    def think(self):
        self.bullet.think()

    @staticmethod
    def from_state(state: dict, material: BaseMaterial = None, mesh: Mesh = None):
        bullet = Bullet.from_state(state)
        return ClientBullet(bullet, material, mesh)
