from game.client.entities.laser_bullet import LaserBullet
from game.entities.star_ship import StarShip
from game.entities.planet import Planet
from game.client.map_objects.client_planet import ClientPlanet
from game.client.entities.client_star_ship import ClientStarShip
from game.entities.bullet import Bullet

SERVER_REGISTRY_ASSOCIATIONS = {
    "bullet": Bullet,
    "player_starship": StarShip,
    "map_object_planet": Planet
}

CLIENT_REGISTRY_ASSOCIATIONS = {
    "bullet": LaserBullet,
    "player_starship": ClientStarShip,
    "map_object_planet": ClientPlanet
}
