from client.client_engine import ClientEngine
from client.base_material import BaseMaterial
from core.vector3 import Vector3

COLORED_VERTEX_SHADER = """
#version 100
precision highp float;
attribute vec3 position;
uniform mat4 projectionMatrix;
uniform mat4 worldViewMatrix;
uniform mat4 modelViewMatrix;

void main() {
    gl_Position = projectionMatrix * (worldViewMatrix * vec4(position, 1.));
}
"""

COLORED_FRAGMENT_SHADER = """
#version 100
precision highp float;
uniform vec3 color;

void main() {
    gl_FragColor = vec4(color, 1.0);
}
"""


class ColoredMaterial(BaseMaterial):
    def __init__(self, engine: ClientEngine, color: list[float]):
        super(ColoredMaterial, self).__init__(engine, "colored_material",
                                              COLORED_VERTEX_SHADER, COLORED_FRAGMENT_SHADER)

        self.color = color

    def get_uniforms(self) -> list[dict]:
        return [
            {
                "name": "color",
                "type": "3f",
                "value": self.color
            }
        ]
