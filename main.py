import sys
import pygame
from math import *
from core.mesh import Mesh
from core.entities.viewable_entity import ViewableEntity
from core.vector3 import Vector3
import pythree
from core.world import World
from core.registry import Registry
from core.entity import Entity
from client.client_entity import ClientEntity
from client.camera import Camera
from client.materials.default import DefaultMaterial
from client.materials.diffuse import DiffuseMaterial
from client.materials.textured import TexturedMaterial
from client.texture2d import Texture2D
from client.renderers.opengl.opengl_renderer import OpenGLRenderer
from client.client_engine import ClientEngine
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
    (800, 600), flags=pygame.OPENGL | pygame.DOUBLEBUF)

world = World(Registry())
engine = ClientEngine(world)

camera = Camera()

renderer = OpenGLRenderer(800, 600, Camera())

engine.add_module(renderer)

# Setup scene
triangle = pythree.Geometry([
    -1.0, 0.0, -0.5,
    0.0, 0.0,   0.5,
    1.0, 0.0,  -0.5
], uvs=[
    0.0, 0.0,
    0.0, 1.0,
    1.0, 0.0
])

triangle2 = pythree.Geometry([
    -1.0, 0.0, -0.5,
    0.0, 0.0,   0.5,
    1.0, 0.0,  -0.5
], normals=[
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 1.0, 0.0
])

entity = Entity(Vector3(0.0, -4.0, 0.0), "ent_test")
entity2 = Entity(Vector3(0.0, 0.0, 0.0), "ent_test2")

client_entity = ClientEntity(entity, "client_ent_test",
                             TexturedMaterial(engine, texture=Texture2D(
                                 0, 0, engine).load_from_file("./texture.png")),
                             Mesh(triangle, engine), rotation=Vector3(0, 0.00, 0))
client_entity2 = ClientEntity(entity2, "client_ent_test2", DefaultMaterial(
    engine), Mesh(triangle2, engine), rotation=Vector3(0, 0.00, 0), scale=Vector3(10))

world.add_entity(client_entity)
world.add_entity(client_entity2)

frame = 0

while True:
    engine.tick()

    entity.position.y = sin(frame / 60 * 2 * pi) + 1.0
    client_entity.rotation.x += 120.0 / 60.0 * pi / 180.0
    client_entity.rotation.y += 60.0 / 60.0 * pi / 180.0
    client_entity.rotation.z += 30.0 / 60.0 * pi / 180.0

    mouse_pos = pygame.mouse.get_pos()

    if keys[pygame.key.key_code('q')]:
        camera.look_at(entity.position)
    else:
        camera.rotation.y = mouse_pos[0] / 800 * pi * 2 - pi
        camera.rotation.x = mouse_pos[1] / 600 * pi * 2 - pi

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
