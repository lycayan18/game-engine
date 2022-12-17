from core.entity import Entity
from core.mesh import Mesh
from core.vector3 import Vector3


class ViewableEntity(Entity):
    def __init__(self, class_name: str, position: Vector3 = Vector3(0, 0, 0), mesh: Mesh = None, rotation: Vector3 = Vector3(0, 0, 0), scale: Vector3 = Vector3(1, 1, 1)):
        super().__init__(position, class_name)
        self.mesh = mesh
        self.rotation = rotation
        self.scale = scale

    def set_mesh(self, mesh: Mesh):
        self.mesh = mesh

    def get_mesh(self):
        return self.mesh

    def set_rotation(self, rotation: Vector3):
        self.rotation = rotation

    def get_rotation(self):
        return self.rotation

    def set_scale(self, scale: Vector3):
        self.scale = scale

    def get_scale(self):
        return self.scale

    def set_state(self, state: dict):
        super(Entity, self).set_state(state)

        self.rotation = Vector3(
            state['rotation']['x'], state['rotation']['y'], self['rotation']['z'])
        self.scale = Vector3(
            state['scale']['x'], state['scale']['y'], self['scale']['z'])

    def get_state(self) -> dict:
        state = {
            **super(Entity, self).get_state(),
            'rotation': {
                'x': self.rotation.x,
                'y': self.rotation.y,
                'z': self.rotation.z
            },
            'scale': {
                'x': self.scale.x,
                'y': self.scale.y,
                'z': self.scale.z
            }
        }

        return state

    @staticmethod
    def from_state(state: dict):
        ent = ViewableEntity(state['class_name'], Vector3(0, 0, 0))

        ent.set_state(state)

        return ent
