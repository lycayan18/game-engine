import pygame
from core.utils.event_emitter import EventEmitter
from core.world import World
from core.module import BaseModule
from client.camera import Camera
from client.entities.sound_entity import SoundEntity
from client.sound_modules.pygame.sound import PygameSound
from client.sound_modules.pos_to_stereo import get_stereo_coefficients_from_position


class PygameSoundModule(BaseModule):
    def __init__(self, camera: Camera):
        super(PygameSoundModule, self).__init__()
        self.camera = camera

    def set_camera(self, camera: Camera):
        self.camera = camera

    def get_camera(self) -> Camera:
        return self.camera

    def init_module(self, world: World, event_emitter: EventEmitter):
        super(PygameSoundModule, self).init_module(world, event_emitter)

        self.event_emitter.on("tick", self.tick)

    def tick(self):
        for entity in self.world.entities:
            if isinstance(entity, SoundEntity):
                sound = entity.get_sound()

                if isinstance(sound, PygameSound):
                    left = 1.0
                    right = 1.0

                    if entity.is_propagatable():
                        left, right = get_stereo_coefficients_from_position(
                            entity.position, self.camera)

                    volume = entity.get_volume()

                    sound.set_volume(left * volume, right * volume)
                    sound.check_for_end()
