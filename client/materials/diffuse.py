from client.client_engine import ClientEngine
from client.base_material import BaseMaterial
from core.vector3 import Vector3

DIFFUSE_VERTEX_SHADER = """
#version 100
precision highp float;
attribute vec3 position;
attribute vec3 normal;
uniform mat4 projectionMatrix;
uniform mat4 worldViewMatrix;
uniform mat4 modelViewMatrix;

varying vec3 vNormal;

void main() {
    vNormal = normalize((modelViewMatrix * vec4(normal, 0.)).xyz);

    gl_Position = projectionMatrix * (worldViewMatrix * vec4(position, 1.));
}
"""

DIFFUSE_FRAGMENT_SHADER = """
#version 100
precision highp float;
uniform vec3 color;
uniform vec3 sunDirection;

varying vec3 vNormal;

void main() {
    float diffuse = max(0.0, dot(vNormal, sunDirection));

    gl_FragColor = vec4(color * diffuse, 1.0);
}
"""


class DiffuseMaterial(BaseMaterial):
    def __init__(self, engine: ClientEngine, sun_direction: Vector3, color: list[float]):
        super(DiffuseMaterial, self).__init__(engine, "diffuse_material",
                                              DIFFUSE_VERTEX_SHADER, DIFFUSE_FRAGMENT_SHADER)

        self.sun_direction = sun_direction
        self.color = color

    def get_uniforms(self) -> list[dict]:
        return [
            {
                "name": "sunDirection",
                "type": "3f",
                "value": [self.sun_direction.x, self.sun_direction.y, self.sun_direction.z]
            },
            {
                "name": "color",
                "type": "3f",
                "value": self.color
            }
        ]
