from core.entities.viewable_map_object import ViewableMapObject
from core.map_object import MapObject
from core.vector3 import Vector3
from core.mesh import Mesh
from client.base_material import BaseMaterial
from client.materials.default import DefaultMaterial


class ClientMapObject(ViewableMapObject):
    def __init__(self, map_object: MapObject, class_name: str, material: BaseMaterial, mesh: Mesh = None,
                 rotation: Vector3 = None, scale: Vector3 = None, visible: bool = True):

        rotation = rotation or Vector3(0, 0, 0)
        scale = scale or Vector3(1, 1, 1)

        super().__init__(class_name, map_object.position, mesh, rotation, scale)

        self.material = material
        self.visible = visible
        self.map_object = map_object

    def get_material(self):
        return self.material

    def get_state(self) -> dict:
        state = {
            **super().get_state(),
            'entity_state': self.map_object.get_state()
        }

        return state

    def set_state(self, state: dict):
        super(ViewableMapObject, self).set_state(state)
        self.map_object.set_state(state['entity_state'])
