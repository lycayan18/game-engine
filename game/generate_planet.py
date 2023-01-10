from random import randint

from core.world import World
from game.entities.planet import Planet
from core.vector3 import Vector3


def generate_planet(world: World, planet_count: int):
    for _ in range(planet_count):
        position = Vector3(randint(-10000, 10000), randint(-10000, 10000), randint(-10000, 10000))
        planet = Planet(world, radius=randint(100, 500), weight=randint(1000000, 5000000), position=position,
                        class_name='map_object_planet')

        world.add_map_object(planet)
