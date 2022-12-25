from core.utils.event_emitter import EventEmitter
from core.world import World
from core.module import BaseModule


class Engine:
    def __init__(self, world: World):
        self.world = world
        self.event_emitter = EventEmitter()
        self.modules = list()

    def add_module(self, module: BaseModule):
        module.init_module(self.world, self.event_emitter)

        self.modules.append(module)

    def register_mesh(self, mesh):
        self.event_emitter.emit("new_mesh", mesh)

    def tick(self):
        self.event_emitter.emit("tick")
        self.world.tick()
