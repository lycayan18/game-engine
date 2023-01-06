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
from client.camera import Camera
from client.renderers.opengl.opengl_renderer import OpenGLRenderer
from OpenGL.GL import *
import glm

keys = [0 for _ in range(255)]

clock = pygame.time.Clock()

pygame.init()
pygame.font.init()
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
pygame.display.gl_set_attribute(
    pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
pygame.display.set_mode(
    (1920, 1080), flags=pygame.OPENGL | pygame.DOUBLEBUF)

world = World(Registry())
engine = Engine(world)

camera = Camera()

renderer = OpenGLRenderer(1920, 1080, Camera())

engine.add_module(renderer)

# Setup scene
triangle = pythree.Geometry([
    -1.0, 0.0, -0.5,
    0.0, 0.0,   0.5,
    1.0, 0.0,  -0.5
])
triangle2 = pythree.Geometry([
    -1.0, 0.0, -0.5,
    0.0, 0.0,   0.5,
    1.0, 0.0,  -0.5
])

entity = ViewableEntity("ent_test", Vector3(
    0.0, -4.0, 0.0), Mesh(triangle, engine), rotation=Vector3(0, 0.00, 0))

entity2 = ViewableEntity("ent_test2", Vector3(
    0.0, 0.0, 0.0), Mesh(triangle2, engine), scale=Vector3(10, 10, 10), rotation=Vector3(0, 0.00, 0))

world.add_entity(entity2)
world.add_entity(entity)

frame = 0

while True:
    engine.tick()

    entity.position.y = sin(frame / 60 * 2 * pi) + 1.0
    entity.rotation.x += 120.0 / 60.0 * pi / 180.0
    entity.rotation.y += 60.0 / 60.0 * pi / 180.0
    entity.rotation.z += 30.0 / 60.0 * pi / 180.0

    mouse_pos = pygame.mouse.get_pos()

    if keys[pygame.key.key_code('q')]:
        camera.look_at(entity.position)
    else:
        camera.rotation.y = mouse_pos[0] / 3840 * pi * 2 - pi
        camera.rotation.x = mouse_pos[1] / 2160 * pi * 2 - pi

    forward = glm.vec3(0.0, 0.0, 1.0)

    forward = glm.rotate(forward, camera.rotation.x,
                         glm.vec3(1.0, 0.0, 0.0))
    forward = glm.rotate(forward, camera.rotation.y,
                         glm.vec3(0.0, 1.0, 0.0))

    left = glm.vec3(1.0, 0.0, 0.0)

    left = glm.rotate(left, camera.rotation.y,
                      glm.vec3(0.0, 1.0, 0.0))

    if keys[pygame.key.key_code('w')]:
        camera.position.x += forward.x * 5.0 / 60.0
        camera.position.y += forward.y * 5.0 / 60.0
        camera.position.z += forward.z * 5.0 / 60.0

    if keys[pygame.key.key_code('s')]:
        camera.position.x -= forward.x * 5.0 / 60.0
        camera.position.y -= forward.y * 5.0 / 60.0
        camera.position.z -= forward.z * 5.0 / 60.0

    if keys[pygame.key.key_code('a')]:
        camera.position.x -= left.x * 5.0 / 60.0
        camera.position.z -= left.z * 5.0 / 60.0

    if keys[pygame.key.key_code('d')]:
        camera.position.x += left.x * 5.0 / 60.0
        camera.position.z += left.z * 5.0 / 60.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            keys[event.key] = True
        elif event.type == pygame.KEYUP:
            keys[event.key] = False

    pygame.display.flip()

    clock.tick(60)

    frame += 1
