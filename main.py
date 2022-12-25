import sys
import pygame
from math import *
from core.mesh import Mesh
from core.entities.viewable_entity import ViewableEntity
from core.vector3 import Vector3
import pythree
from core.world import World
from core.engine import Engine
from core.registry import Registry
from client.renderers.opengl.opengl_renderer import OpenGLRenderer

keys = [0 for _ in range(255)]

pygame.init()
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
pygame.display.gl_set_attribute(
    pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
pygame.display.set_mode((640, 480), flags=pygame.OPENGL | pygame.DOUBLEBUF)

world = World(Registry())
engine = Engine(world)

renderer = OpenGLRenderer(640, 480)

engine.add_module(renderer)

# Setup scene
triangle = pythree.Geometry([
    -1.0, 0.0, -0.5,
    0.0, 0.0,   0.5,
    1.0, 0.0,  -0.5
])

entity = ViewableEntity("ent_test", Vector3(
    0.0, -4.0, 5.0), Mesh(triangle, engine))

world.add_entity(entity)


while True:
    engine.tick()

    if keys[pygame.key.key_code('w')]:
        entity.position.x -= sin(-entity.rotation.y) * 5.0 / 60.0
        entity.position.z -= cos(-entity.rotation.y) * 5.0 / 60.0

    if keys[pygame.key.key_code('s')]:
        entity.position.x += sin(-entity.rotation.y) * 5.0 / 60.0
        entity.position.z += cos(-entity.rotation.y) * 5.0 / 60.0

    if keys[pygame.key.key_code('a')]:
        entity.rotation.y += 120.0 / 60.0 * pi / 180

    if keys[pygame.key.key_code('d')]:
        entity.rotation.y -= 120.0 / 60.0 * pi / 180

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            keys[event.key] = True
        elif event.type == pygame.KEYUP:
            keys[event.key] = False

    pygame.display.flip()
    pygame.time.wait(16)
