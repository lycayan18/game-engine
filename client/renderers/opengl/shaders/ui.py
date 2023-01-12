from client.client_engine import ClientEngine
from client.base_material import BaseMaterial
from client.texture2d import Texture2D

FREE_TEXTURED_VERTEX_SHADER = """
#version 100
precision highp float;
attribute vec3 position;

void main() {
    gl_Position = vec4(position, 1.);
}
"""

FREE_TEXTURED_FRAGMENT_SHADER = """
#version 100
precision highp float;
uniform sampler2D textureSampler;
uniform vec2 screenSize;

void main() {
    vec4 color = texture2D(textureSampler, gl_FragCoord.xy / screenSize, 0.0);

    gl_FragColor = color;
}
"""
