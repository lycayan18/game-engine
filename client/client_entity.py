from core.entities.viewable_entity import ViewableEntity
from core.entity import Entity
from core.vector3 import Vector3
from core.mesh import Mesh
from client.base_material import BaseMaterial
from client.materials.default import DefaultMaterial


class ClientEntity(ViewableEntity):
    def __init__(self, entity: Entity, class_name: str, material: BaseMaterial, mesh: Mesh = None,
                 rotation: Vector3 = None, scale: Vector3 = None):

        self.rotation = rotation or Vector3(0, 0, 0)
        self.scale = scale or Vector3(1, 1, 1)

        super().__init__(class_name, entity.position, mesh, self.rotation, self.scale)

        self.material = material

        self.entity = entity

    def get_material(self):
        return self.material

    def set_position(self, position: Vector3):
        super(ClientEntity, self).set_position(position)

        self.entity.set_position(position)

    def get_position(self) -> Vector3:
        return self.entity.get_position()

    def get_state(self) -> dict:
        state = {
            **super(ClientEntity, self).get_state(),
            'entity_state': self.entity.get_state()
        }

        return state

    def set_state(self, state: dict):
        super(ClientEntity, self).set_state(state)
        self.entity.set_state(state['entity_state'])
