from random import randint

from core.vector3 import Vector3
from core.world import World
from game.entities.planet import Planet
from game.entities.star_ship import StarShip
from game.weapons.laser_gun import LaserGun
from game.constants.world_size import SIZE


def create_valid_position(world: World):
    while True:
        position = Vector3(randint(*SIZE), randint(*SIZE), randint(*SIZE))

        is_valid_position = True

        for map_object in world.map_objects:
            if isinstance(map_object, Planet):
                if map_object.get_collision_model().collide_point(position):
                    is_valid_position = False
                    break

        for entity in world.entities:
            if isinstance(entity, Planet):
                if entity.get_collision_model().collide_point(position):
                    is_valid_position = False

        if is_valid_position:
            return position


def generate_star_ship(world: World, id: int = 0) -> StarShip:
    position = create_valid_position(world)

    star_ship = StarShip(weapon=LaserGun(
        world), position=position, class_name="player_starship")
    star_ship.id = id

    return star_ship