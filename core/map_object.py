from core.vector3 import Vector3


class MapObject:
    def __init__(self, vector: Vector3, class_name: str):
        self.vector = vector
        self.class_name = class_name
        self.id = 0

    def set_state(self, state: dict):
        x = state.get('x')
        y = state.get('y')
        z = state.get('z')
        self.vector = Vector3(x, y, z)
        self.class_name = state.get('class_name', None)

    def get_state(self):
        state = {
            'x': self.vector.x,
            'y': self.vector.y,
            'z': self.vector.z,
            'class_name': self.class_name
        }

        return state

    def think(self):
        pass

    @staticmethod
    def from_state(state: dict):
        map_object = MapObject(Vector3(0, 0, 0), "")

        map_object.set_state(state)

        return map_object
