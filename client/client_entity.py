from core.entities.viewable_entity import ViewableEntity
from core.entity import Entity
from core.vector3 import Vector3
from core.mesh import Mesh


class ClientEntity(ViewableEntity):
    def __init__(self, entity: Entity, class_name: str, mesh: Mesh = None,
                 rotation: Vector3 = None, scale: Vector3 = None):

        rotation = rotation or Vector3(0, 0, 0)
        scale = scale or Vector3(1, 1, 1)

        super().__init__(class_name, entity.position, mesh, rotation, scale)
        self.entity = entity

    def get_state(self) -> dict:
        state = {
            **super().get_state(),
            'entity_state': self.entity.get_state()
        }

        return state

    def set_state(self, state: dict):
        super(ClientEntity, self).set_state(state)
        self.entity.set_state(state['entity_state'])
