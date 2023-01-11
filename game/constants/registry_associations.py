from game.entities.star_ship import StarShip
from game.entities.planet import Planet
from game.client.entities.client_star_ship import ClientStarShip
from game.entities.bullet import Bullet

SERVER_REGISTRY_ASSOCIATIONS = {
    "bullet": Bullet,
    "player_starship": StarShip,
    "mapobj_planet": Planet
}

CLIENT_REGISTRY_ASSOCIATIONS = {
    "bullet": Bullet,
    "player_starship": ClientStarShip,
    "mapobj_planet": Planet
}
