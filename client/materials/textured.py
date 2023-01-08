from client.client_engine import ClientEngine
from client.base_material import BaseMaterial
from client.texture2d import Texture2D

TEXTURED_VERTEX_SHADER = """
#version 100
precision highp float;
attribute vec3 position;
attribute vec2 uv;
uniform mat4 projectionMatrix;
uniform mat4 worldViewMatrix;

varying vec2 vUv;

void main() {
    vUv = uv;

    gl_Position = projectionMatrix * (worldViewMatrix * vec4(position, 1.));
}
"""

TEXTURED_FRAGMENT_SHADER = """
#version 100
precision highp float;
uniform sampler2D textureSampler;

varying vec2 vUv;

void main() {
    gl_FragColor = texture2D(textureSampler, vUv, 0.0);
}
"""


class TexturedMaterial(BaseMaterial):
    def __init__(self, engine: ClientEngine, texture: Texture2D):
        super(TexturedMaterial, self).__init__(engine, "textured_material",
                                               TEXTURED_VERTEX_SHADER, TEXTURED_FRAGMENT_SHADER)

        self.texture = texture

    def get_uniforms(self) -> list[dict]:
        return [
            {
                "name": "textureSampler",
                "type": "texture2D",
                "value": self.texture
            }
        ]
