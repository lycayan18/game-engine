from random import randint

from core.vector3 import Vector3
from core.world import World
from game.entities.planet import Planet
from game.entities.star_ship import StarShip
from game.weapons.laser_gun import LaserGun
from game.constants.world_size import SIZE


def generate_star_ship(world: World, id: int = 0) -> StarShip:
    while True:
        position = Vector3(randint(*SIZE), randint(*SIZE), randint(*SIZE))
        for entity in world.entities:
            if isinstance(entity, Planet):
                if entity.get_collision_model().collide_point(position):
                    continue

        break

    star_ship = StarShip(weapon=LaserGun(world), position=position)
    star_ship.id = id

    return star_ship
