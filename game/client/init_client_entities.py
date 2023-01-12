from core.vector3 import Vector3
from core.mesh import Mesh
from client.materials.diffuse import DiffuseMaterial
from game.client.entities.laser_bullet import LaserBullet
from game.lib.mesh_generator.box import generate_box
from game.client.entities.client_star_ship import ClientStarShip
from game.client.main_client import Client


def init_client_entities(engine: Client):
    """
    Setups static variables for client entities such as materials, sounds, etc.
    """

    ClientStarShip.mesh = Mesh(generate_box(
        Vector3(1.214 * 0.25, 0.8 * 0.25, 2.0 * 0.25)), engine)
    ClientStarShip.material = DiffuseMaterial(
        engine, Vector3(0, 0, -1), [1, 1, 1])

    LaserBullet.mesh = Mesh(generate_box(Vector3(0.1)), engine)
    LaserBullet.material = DiffuseMaterial(
        engine, Vector3(0, 0, -1), [1, 1, 1])
