from core.vector3 import Vector3


class Entity:
    def __init__(self, position: Vector3, class_name: str):
        self.position = position
        self.class_name = class_name
        self.id = 0
        self.last_events = []

        self.deleted = False

    def delete(self):
        self.deleted = True

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

    def push_event(self, event: dict):
        """
        Pushes event to the event list. Just to keep away from accessing entities' props and work with getters and setters.
        Useful for using in class methods, e.g. in realisation of RocketEntity's "explode" method.
        Not useful for using outside the class methods, e.g. "rocket.push_event(...)" - this function is not about this case.
        """

        self.last_events.append(event)

    def get_last_events(self) -> list[dict]:
        # Copy the events list to avoid returning link to the list which have been already cleared
        events = self.last_events[:]

        self.last_events.clear()

        return events

    def emit_events(self, events: list[dict]):
        pass

    def think(self):
        pass

    @staticmethod
    def from_state(state: dict):
        entity = Entity(Vector3(0, 0, 0), state['class_name'])

        entity.set_state(state)

        return entity
