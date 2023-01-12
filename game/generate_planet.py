from random import randint

from core.world import World
from game.entities.planet import Planet
from core.vector3 import Vector3


def generate_planet(world: World, planet_count: int):
    for _ in range(planet_count):
        position = Vector3(randint(-500, 500),
                           randint(-500, 500), randint(-500, 500))

        radius = randint(30, 50)

        planet = Planet(world, radius=radius, weight=radius * 50, position=position,
                        class_name='map_object_planet')

        world.add_map_object(planet)
