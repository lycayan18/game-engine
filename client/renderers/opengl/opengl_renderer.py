import struct
import ctypes
import glm
from OpenGL.GL import *

from client.client_map_object import ClientMapObject
from core.mesh import Mesh
from core.module import BaseModule
from core.utils.event_emitter import EventEmitter
from core.world import World
from client.client_entity import ClientEntity
from client.graphics_module import GraphicsModule
from client.camera import Camera
from client.base_material import BaseMaterial
from client.texture2d import Texture2D


class OpenGLRenderer(GraphicsModule):
    def __init__(self, width: int, height: int, camera: Camera):
        super(OpenGLRenderer, self).__init__(camera)

        self.buffer_mesh_pairs = []
        self.width = width
        self.height = height
        self.shaders: dict = {}
        self.textures: list[dict] = []

        self.init_gl()

    def init_module(self, world: World, event_emitter: EventEmitter):
        super().init_module(world, event_emitter)

        event_emitter.on("new_mesh", self.handle_new_mesh)
        event_emitter.on("tick", self.draw)
        event_emitter.on("material_registered", self.register_material)
        event_emitter.on("texture_registered", self.register_texture)

    def init_gl(self):
        vao = GLuint(0)

        glGenVertexArrays(1, vao)
        glBindVertexArray(vao.value)

        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LEQUAL)

    def register_material(self, material: BaseMaterial):
        name = material.get_name()

        if name in self.shaders:
            return

        shader = self.create_shader(
            material.get_vertex_source(), material.get_fragment_source())

        self.shaders[name] = shader

    def register_texture(self, texture: Texture2D):
        buffer = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, buffer)

        data = texture.get_data()

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, *texture.get_size(),
                     0, GL_RGBA, GL_UNSIGNED_BYTE, data)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                        GL_LINEAR_MIPMAP_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glGenerateMipmap(GL_TEXTURE_2D)

        self.textures.append({
            "texture": texture,
            "buffer": buffer
        })

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
        glClearDepth(1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

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

        for entity in self.world.entities + self.world.map_objects:
            if isinstance(entity, ClientEntity) or isinstance(entity, ClientMapObject):
                # *************************************************
                # * Generate matrices
                # *************************************************

                material = entity.get_material()
                program = self.shaders[material.get_name()]

                # print(program)

                glUseProgram(program)

                position_location = glGetAttribLocation(
                    program, "position")

                normal_location = glGetAttribLocation(
                    program, "normal")

                uv_location = glGetAttribLocation(
                    program, "uv")

                projection_matrix_location = glGetUniformLocation(
                    program, "projectionMatrix")

                world_view_matrix_location = glGetUniformLocation(
                    program, "worldViewMatrix")

                model_view_matrix_location = glGetUniformLocation(
                    program, "modelViewMatrix")

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
                # * Setup material uniforms
                # *************************************************

                active_texture = 0

                for uniform in material.get_uniforms():
                    location = glGetUniformLocation(program, uniform["name"])

                    active_texture = self.set_uniform_value(
                        location, uniform["value"], uniform["type"], active_texture)

                # *************************************************
                # * Draw entity
                # *************************************************

                # Search buffer
                for vertex_buffer, normals_buffer, uvs_buffer, mesh in self.buffer_mesh_pairs:
                    if mesh == entity.mesh:
                        if normal_location > -1:
                            glBindBuffer(GL_ARRAY_BUFFER, normals_buffer)
                            glVertexAttribPointer(
                                normal_location, 3, GL_FLOAT, True, 0, ctypes.c_void_p(0))
                            glEnableVertexAttribArray(normal_location)

                        if uv_location > -1:
                            glBindBuffer(GL_ARRAY_BUFFER, uvs_buffer)
                            glVertexAttribPointer(
                                uv_location, 2, GL_FLOAT, True, 0, ctypes.c_void_p(0))
                            glEnableVertexAttribArray(uv_location)

                        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
                        glEnableVertexAttribArray(position_location)
                        glVertexAttribPointer(
                            position_location, 3, GL_FLOAT, False, 0, ctypes.c_void_p(0))
                        break

                glDrawArrays(GL_TRIANGLES, 0, int(len(
                    entity.mesh.geometry.get_vertices()) / 3))

    def set_uniform_value(self, location, value, type: str, active_texture: int = 0):
        if type in ["1f", "1fv"]:
            glUniform1f(location, value)
        elif type in ["2f", "2fv"]:
            glUniform2fv(location, 1, value)
        elif type in ["3f", "3fv"]:
            glUniform3fv(location, 1, value)
        elif type in ["4f", "4fv"]:
            glUniform4fv(location, 1, value)
        elif type in ["i1", "i1v"]:
            glUniform1i(location, value)
        elif type in ["i2", "i2v"]:
            glUniform2iv(location, 1, value)
        elif type in ["i3", "i3v"]:
            glUniform3iv(location, 1, value)
        elif type in ["i4", "i4v"]:
            glUniform4iv(location, 1, value)
        elif type == "mat2":
            glUniformMatrix2fv(location, False, value)
        elif type == "mat3":
            glUniformMatrix3fv(location, False, value)
        elif type == "mat4":
            glUniformMatrix4fv(location, False, value)
        elif type == "texture2D":
            glActiveTexture(GL_TEXTURE0 + active_texture)

            for texture in self.textures:
                # Comparing links
                if texture["texture"] == value:
                    glBindTexture(GL_TEXTURE_2D, texture["buffer"])
                    break

            glUniform1i(location, active_texture)

            return active_texture + 1

        # Returns current active texture in case we have two or more textures at the same time
        return active_texture

    def handle_new_mesh(self, mesh: Mesh):
        vertex_data = mesh.geometry.get_vertices_as_bytes()
        normals_data = mesh.geometry.get_normals_as_bytes()
        uvs_data = mesh.geometry.get_uvs_as_bytes()

        vertex_buffer = self.generate_array_buffer(vertex_data)
        normals_buffer = self.generate_array_buffer(normals_data)
        uvs_buffer = self.generate_array_buffer(uvs_data)

        self.buffer_mesh_pairs.append(
            (vertex_buffer, normals_buffer, uvs_buffer, mesh))

    def generate_array_buffer(self, data: bytes):
        buffer = glGenBuffers(1)

        glBindBuffer(GL_ARRAY_BUFFER, buffer)

        glBufferData(GL_ARRAY_BUFFER, len(data), data, GL_DYNAMIC_DRAW)

        return buffer
