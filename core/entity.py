from core.vector3 import Vector3


class Entity:
    def __init__(self, position: Vector3, class_name: str):
        self.position = position
        self.class_name = class_name
        self.id = 0

    def set_position(self, position: Vector3):
        self.position = position

    def get_position(self):
        return self.position

    def set_state(self, state: dict):
        self.position = Vector3(
            state['position']['x'], state['position']['y'], state['position']['z'])
        self.class_name = state.get('class_name', self.class_name)
        self.id = state.get('id', 0)

    def get_state(self):
        state = {
            'position': {
                'x': self.position.x,
                'y': self.position.y,
                'z': self.position.z
            },
            'class_name': self.class_name,
            'id': self.id
        }

        return state

    def think(self):
        pass

    @staticmethod
    def from_state(state: dict):
        entity = Entity(Vector3(0, 0, 0), state['class_name'])

        entity.set_state(state)

        return entity
