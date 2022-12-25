from core.world import World
from core.utils.event_emitter import EventEmitter


class BaseModule:
    def __init__(self):
        self.world: World = None
        self.event_emitter: EventEmitter = None

    def init_module(self, world: World, event_emitter: EventEmitter):
        self.world = world
        self.event_emitter = event_emitter
