import ctypes
import glm
from OpenGL.GL import *
from core.entities.viewable_entity import ViewableEntity
from core.mesh import Mesh
from core.module import BaseModule
from core.utils.event_emitter import EventEmitter
from core.world import World
from client.graphics_module import GraphicsModule
from client.camera import Camera

BASE_VERTEX_SHADER = """
#version 100
precision highp float;
attribute vec3 position;
uniform mat4 projectionMatrix;
uniform mat4 worldViewMatrix;

void main(){
    gl_Position = projectionMatrix * (worldViewMatrix * vec4(position, 1.));
}
"""
BASE_FRAGMENT_SHADER = """
#version 100
precision highp float;

void main() {
    gl_FragColor = vec4(0.0, 1.0, 1.0, 1.0);
}
"""


class OpenGLRenderer(GraphicsModule):
    def __init__(self, width: int, height: int, camera: Camera):
        super(OpenGLRenderer, self).__init__(camera)

        self.program = None
        self.buffer_mesh_pairs = []
        self.width = width
        self.height = height

        self.init_gl()

    def init_module(self, world: World, event_emitter: EventEmitter):
        super().init_module(world, event_emitter)

        event_emitter.on("new_mesh", self.handle_new_mesh)
        event_emitter.on("tick", self.draw)

    def init_gl(self):
        program = self.create_shader(BASE_VERTEX_SHADER, BASE_FRAGMENT_SHADER)

        self.program = program

        glUseProgram(program)

        vao = GLuint(0)

        glGenVertexArrays(1, vao)
        glBindVertexArray(vao.value)

    def create_shader(self, vertex_source: str, fragment_source: str):
        vertex = glCreateShader(GL_VERTEX_SHADER)
        fragment = glCreateShader(GL_FRAGMENT_SHADER)

        glShaderSource(vertex, vertex_source)
        glShaderSource(fragment, fragment_source)

        glCompileShader(vertex)

        if not glGetShaderiv(vertex, GL_COMPILE_STATUS):
            log = glGetShaderInfoLog(vertex).decode()

            raise RuntimeError("Cannot compile vertex shader:\n", log)

        glCompileShader(fragment)

        if not glGetShaderiv(fragment, GL_COMPILE_STATUS):
            log = glGetShaderInfoLog(fragment).decode()

            raise RuntimeError("Cannot compile fragment shader:\n", log)

        program = glCreateProgram()
        glAttachShader(program, vertex)
        glAttachShader(program, fragment)
        glLinkProgram(program)

        if not glGetProgramiv(program, GL_LINK_STATUS):
            log = glGetProgramInfoLog(program)

            raise RuntimeError("Cannot link program:\n", log)

        glDetachShader(program, vertex)
        glDetachShader(program, fragment)

        return program

    def create_texture2D(self, width: int, height: int, data: bytes):
        buffer = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, buffer)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width,
                     height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                        GL_NEAREST_MIPMAP_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        glGenerateMipmap(GL_TEXTURE_2D)

        return buffer

    def draw(self):
        glClearColor(0.0, 0.0, 0.3, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        if self.program is None:
            return

        projection_matrix = glm.perspective(
            glm.radians(90), self.width / self.height, 0.1, 100.0)

        # Create camera view matrix

        camera = self.get_camera()

        camera_view_matrix = glm.mat4x4()

        # Rotate

        camera_rotation = camera.get_rotation()

        camera_view_matrix = glm.rotate(camera_view_matrix, camera_rotation.x, glm.vec3(
            1.0, 0.0, 0.0
        ))

        camera_view_matrix = glm.rotate(camera_view_matrix, camera_rotation.y, glm.vec3(
            0.0, 1.0, 0.0
        ))

        camera_view_matrix = glm.rotate(camera_view_matrix, camera_rotation.z, glm.vec3(
            0.0, 0.0, 1.0
        ))

        camera_position = camera.get_position()

        # Translate

        camera_rotation = camera.get_rotation()

        camera_view_matrix = glm.translate(camera_view_matrix, glm.vec3(
            -camera_position.x, -camera_position.y, camera_position.z
        ))

        for entity in self.world.entities:
            if isinstance(entity, ViewableEntity):
                # *************************************************
                # * Generate matrices
                # *************************************************

                glUseProgram(self.program)

                position_location = glGetAttribLocation(
                    self.program, "position")
                projection_matrix_location = glGetUniformLocation(
                    self.program, "projectionMatrix")
                world_view_matrix_location = glGetUniformLocation(
                    self.program, "worldViewMatrix")
                model_view_matrix_location = glGetUniformLocation(
                    self.program, "modelViewMatrix")

                glUniformMatrix4fv(projection_matrix_location,
                                   1, False, projection_matrix.to_bytes())

                world_view_matrix: glm.mat4x4 = glm.mat4x4(camera_view_matrix)

                world_view_matrix = glm.translate(world_view_matrix, glm.vec3(
                    entity.position.x, entity.position.y, -entity.position.z))

                world_view_matrix = glm.rotate(world_view_matrix, entity.rotation.x,
                                               glm.vec3(1.0, 0.0, 0.0))
                world_view_matrix = glm.rotate(world_view_matrix, entity.rotation.y,
                                               glm.vec3(0.0, 1.0, 0.0))
                world_view_matrix = glm.rotate(world_view_matrix, entity.rotation.z,
                                               glm.vec3(0.0, 0.0, 1.0))

                world_view_matrix = glm.scale(world_view_matrix, glm.vec3(
                    entity.scale.x, entity.scale.y, entity.scale.z))

                glUniformMatrix4fv(world_view_matrix_location,
                                   1, False, world_view_matrix.to_bytes())

                model_view_matrix: glm.mat4x4 = glm.mat4x4()

                model_view_matrix = glm.translate(model_view_matrix, glm.vec3(
                    entity.position.x, entity.position.y, -entity.position.z))

                model_view_matrix = glm.rotate(model_view_matrix, entity.rotation.x,
                                               glm.vec3(1.0, 0.0, 0.0))
                model_view_matrix = glm.rotate(model_view_matrix, entity.rotation.y,
                                               glm.vec3(0.0, 1.0, 0.0))
                model_view_matrix = glm.rotate(model_view_matrix, entity.rotation.z,
                                               glm.vec3(0.0, 0.0, 1.0))

                model_view_matrix = glm.scale(model_view_matrix, glm.vec3(
                    entity.scale.x, entity.scale.y, entity.scale.z))

                glUniformMatrix4fv(model_view_matrix_location,
                                   1, False, model_view_matrix.to_bytes())

                # *************************************************
                # * Draw entity
                # *************************************************

                # Search buffer
                for buffer, mesh in self.buffer_mesh_pairs:
                    if mesh == entity.mesh:
                        glBindBuffer(GL_ARRAY_BUFFER, buffer)
                        break

                glEnableVertexAttribArray(position_location)
                glVertexAttribPointer(
                    position_location, 3, GL_FLOAT, False, 0, ctypes.c_void_p(0))
                glDrawArrays(GL_TRIANGLES, 0, int(len(
                    entity.mesh.geometry.get_vertices()) / 3))

    def handle_new_mesh(self, mesh: Mesh):
        vertex_data = mesh.geometry.get_vertices_as_bytes()

        vertex_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)

        print(vertex_data)
        print(len(vertex_data))

        glBufferData(GL_ARRAY_BUFFER, len(vertex_data),
                     vertex_data, GL_DYNAMIC_DRAW)

        self.buffer_mesh_pairs.append((vertex_buffer, mesh))
