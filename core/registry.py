# Registry associates class_name with Entity/MapObject class, so you can create a new entity
# by its class_name:
# registry = Registry()
# registry.associate("ent_player", Player)
# entity_constructor = registry.get_entity_constructor("ent_player")
# entity = entity_constructor(*args)  - equivalent to ```entity = Player(*args)```
from core.entity import Entity
from core.map_object import MapObject
from typing import Union


class Registry:
    def __init__(self, associates: dict[str, Union[Entity.__class__, MapObject.__class__]] = dict()):
        self.classnames: dict[str, Union[Entity.__class__, MapObject.__class__]] = associates

    def associate(self, class_name: str, constructor: Union[Entity.__class__, MapObject.__class__]):
        self.classnames[class_name] = constructor

    def get_constructor(self, class_name: str, default: Union[Entity.__class__, MapObject.__class__]) -> Union[Entity.__class__, MapObject.__class__]:
        return self.classnames.get(class_name, default)
