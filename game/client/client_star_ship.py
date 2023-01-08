from client.base_material import BaseMaterial
from client.client_entity import ClientEntity
from core.mesh import Mesh
from core.vector3 import Vector3
from game.entities.star_ship import StarShip
from game.entities.weapon import Weapon


class ClientStarShip(ClientEntity):
    def __init__(self, position: Vector3, weapon: Weapon, class_name: str, material: BaseMaterial, mesh: Mesh = None,
                 rotation: Vector3 = None, scale: Vector3 = None):

        rotation = rotation or Vector3(0, 0, 0)
        scale = scale or Vector3(1, 1, 1)

        star_ship = StarShip(weapon, 1000, rotation, class_name, position, 100.0)
        super(ClientStarShip, self).__init__(star_ship, class_name, material, mesh, rotation, scale)

    def play_shoot_sound(self):
        ...

    def dead_animation(self):
        ...

    def dead(self):
        self.entity.dead()
        self.dead_animation()

    def shoot(self):
        self.entity.shoot()
        self.play_shoot_sound()


