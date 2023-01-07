import datetime
from core.utils.event_emitter import EventEmitter
from core.entity import Entity
from core.map_object import MapObject
from core.registry import Registry


class World:
    def __init__(self, registry: Registry):
        self.entities: list[Entity] = []
        self.map_objects: list[MapObject] = []
        self.entity_unique_id = 0  # For generating entity unique id
        self.map_object_unique_id = 0  # For generating map object unique id
        self.registry = registry
        self.event_emitter = EventEmitter()
        self.start_time = datetime.datetime.now()

    def set_state(self, state: dict):
        updated_entities_id: list[int] = list()

        self.entity_unique_id = state.get(
            "entity_unique_id", self.entity_unique_id)
        self.map_object_unique_id = state.get(
            "map_object_unique_id", self.map_object_unique_id)

        entities = state.get('entities')
        map_objects = state.get('map_objects')

        # Update entity states
        for i, entity_state in enumerate(entities):
            # Search entity
            entity = self.get_entity_by_id(entity_state["id"])

            if entity is None:
                # Entity was not found, so create it
                EntityClass = self.registry.get_constructor(
                    entity_state["class_name"], Entity)

                entity = EntityClass.from_state(entity_state)

                self.add_entity(entity, False)

            entity.set_state(entity_state)

            updated_entities_id.append(entity_state["id"])

        # Delete all not included in world state entities
        for entity in self.entities:
            if entity.id not in updated_entities_id:
                self.remove_entity(entity)

        # Update map object states
        for i, map_object_state in enumerate(map_objects):
            # Search map object
            map_object = self.get_map_object_by_id(map_object_state["id"])

            if map_object is None:
                # MapObject was not found, so create it
                MapObjectClass: MapObject = self.registry.get_constructor(
                    map_object_state["class_name"], MapObject)

                map_object = MapObjectClass.from_state(map_object_state)

                self.add_map_object(map_object, False)

            self.map_objects[i].set_state(map_object_state)

    def get_state(self):
        state = {
            'entity_unique_id': self.entity_unique_id,
            'map_object_unique_id': self.map_object_unique_id,
            'entities': [],
            'map_objects': []
        }

        for entity in self.entities:
            state['entities'].append(entity.get_state())

        for map_object in self.map_objects:
            state['map_objects'].append(map_object.get_state())

        return state

    def get_entity_by_id(self, id: int) -> Entity:
        for entity in self.entities:
            if entity.id == id:
                return entity

    def get_map_object_by_id(self, id: int) -> MapObject:
        for map_object in self.map_objects:
            if map_object.id == id:
                return map_object

    def add_entity(self, entity: Entity, needs_id: bool = True):
        if needs_id:
            entity.id = self.entity_unique_id
            self.entity_unique_id += 1

        self.entities.append(entity)

        self.event_emitter.emit("entity_added", entity)

    def add_map_object(self, map_object: MapObject, needs_id: bool = True):
        if needs_id:
            map_object.id = self.map_object_unique_id

            self.map_object_unique_id += 1

        self.map_objects.append(map_object)

        self.event_emitter.emit("map_object_added", map_object)

    def remove_entity(self, entity: Entity):
        self.entities.remove(entity)

        self.event_emitter.emit("entity_removed", entity)

    def remove_map_object(self, map_object: MapObject):
        self.map_objects.remove(map_object)

        self.event_emitter.emit("map_object_removed", map_object)

    def remove_all_entities(self):
        self.entities.clear()

        self.event_emitter.emit("all_entities_removed")

    def remove_all_map_object(self):
        self.map_objects.clear()

        self.event_emitter.emit("all_map_objects_removed")

    def tick(self):
        self.event_emitter.emit("before_tick")

        for entity in self.entities:
            if entity.deleted:
                self.remove_entity(entity)
                continue

            entity.think()

        for object in self.map_objects:
            object.think()

        self.event_emitter.emit("after_tick")

    def get_time(self):
        return self.start_time - datetime.datetime.now()
