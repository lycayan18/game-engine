# Registry associates classname with Entity/MapObject class, so you can create a new entity
# by its classname:
# registry = Registry()
# registry.associate("ent_player", Player)
# entity_constructor = registry.get_entity_constructor("ent_player")
# entity = entity_constructor(*args)  - equivalent to ```entity = Player(*args)```
from core.entity import Entity
from core.map_object import MapObject
from typing import Union


class Registry:
    def __init__(self, associates: dict[str, Union[Entity, MapObject]] = dict()):
        self.classnames: dict[str, Union[Entity, MapObject]] = associates

    def associate(self, classname: str, constructor: Union[Entity, MapObject]):
        self.classnames[classname] = constructor

    def get_constructor(self, classname: str, default: Union[Entity, MapObject]) -> Union[Entity, MapObject]:
        return self.classnames.get(classname, default)
