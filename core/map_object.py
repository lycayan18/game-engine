from core.vector3 import Vector3


class MapObject:
    def __init__(self, position: Vector3, class_name: str):
        self.position = position
        self.class_name = class_name
        self.id = 0

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
        map_object = MapObject(Vector3(0, 0, 0), "")

        map_object.set_state(state)

        return map_object
