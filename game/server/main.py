import pygame
from core.registry import Registry
from game.server.main_server import Server
from game.constants.registry_associations import SERVER_REGISTRY_ASSOCIATIONS

FPS = 60


def main(ip, port):
    clock = pygame.time.Clock()

    server = Server(Registry(SERVER_REGISTRY_ASSOCIATIONS), ip, port)

    while True:
        try:
            server.tick()

            clock.tick(FPS)
        except Exception as e:
            server.shutdown()
            raise e

