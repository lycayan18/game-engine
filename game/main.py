import sys
import pygame
from math import *
from core.mesh import Mesh
from core.entities.viewable_entity import ViewableEntity
from core.vector3 import Vector3
import pythree
from client.camera import Camera
from client.renderers.opengl.opengl_renderer import OpenGLRenderer
import glm
from game.client.client import Client
from core.world import World
from core.registry import Registry
from core.entity import Entity


def main(ip: str, port: int):
    registry = Registry()
    registry.associate('ent_base', Entity)
    client = Client(World(registry), ip, port)

    clock = pygame.time.Clock()

    pygame.init()
    pygame.font.init()
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
    pygame.display.gl_set_attribute(
        pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
    pygame.display.set_mode(
        (1920, 1080), flags=pygame.OPENGL | pygame.DOUBLEBUF)

    camera = Camera()

    renderer = OpenGLRenderer(1920, 1080, Camera())

    client.add_module(renderer)

    triangle = pythree.Geometry([
        -1.0, 0.0, -0.5,
        0.0, 0.0, 0.5,
        1.0, 0.0, -0.5
    ])
    triangle2 = pythree.Geometry([
        -1.0, 0.0, -0.5,
        0.0, 0.0, 0.5,
        1.0, 0.0, -0.5
    ])

    entity = ViewableEntity("ent_test", Vector3(
        0.0, -4.0, 0.0), Mesh(triangle, client), rotation=Vector3(0, 0.00, 0))

    entity2 = ViewableEntity("ent_test2", Vector3(
        0.0, 0.0, 0.0), Mesh(triangle2, client), scale=Vector3(10, 10, 10), rotation=Vector3(0, 0.00, 0))

    client.world.add_entity(entity2)
    client.world.add_entity(entity)

    frame = 0

    while True:
        client.tick()

        entity.position.y = sin(frame / 60 * 2 * pi) + 1.0
        entity.rotation.x += 120.0 / 60.0 * pi / 180.0
        entity.rotation.y += 60.0 / 60.0 * pi / 180.0
        entity.rotation.z += 30.0 / 60.0 * pi / 180.0

        mouse_pos = pygame.mouse.get_pos()

        forward = glm.vec3(0.0, 0.0, 1.0)

        forward = glm.rotate(forward, camera.rotation.x,
                             glm.vec3(1.0, 0.0, 0.0))
        forward = glm.rotate(forward, camera.rotation.y,
                             glm.vec3(0.0, 1.0, 0.0))

        left = glm.vec3(1.0, 0.0, 0.0)

        left = glm.rotate(left, camera.rotation.y,
                          glm.vec3(0.0, 1.0, 0.0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    camera.look_at(entity.position)
                else:
                    camera.rotation.y = mouse_pos[0] / 1920 * pi * 2 - pi
                    camera.rotation.x = mouse_pos[1] / 1080 * pi * 2 - pi

                if event.key == pygame.K_w:
                    camera.position.x += forward.x * 5.0 / 60.0
                    camera.position.y += forward.y * 5.0 / 60.0
                    camera.position.z += forward.z * 5.0 / 60.0

                if event.key == pygame.K_s:
                    camera.position.x -= forward.x * 5.0 / 60.0
                    camera.position.y -= forward.y * 5.0 / 60.0
                    camera.position.z -= forward.z * 5.0 / 60.0

                if event.key == pygame.K_a:
                    camera.position.x -= left.x * 5.0 / 60.0
                    camera.position.z -= left.z * 5.0 / 60.0

                if event.key == pygame.K_w:
                    camera.position.x += left.x * 5.0 / 60.0
                    camera.position.z += left.z * 5.0 / 60.0

        pygame.display.flip()

        clock.tick(60)

        frame += 1