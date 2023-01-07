from client.client_engine import ClientEngine
from client.base_material import BaseMaterial

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


class DefaultMaterial(BaseMaterial):
    def __init__(self, engine: ClientEngine):
        super(DefaultMaterial, self).__init__(
            engine, "default_material", BASE_VERTEX_SHADER, BASE_FRAGMENT_SHADER)
