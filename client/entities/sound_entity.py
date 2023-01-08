from core.vector3 import Vector3
from core.utils.event_emitter import EventEmitter
from core.entity import Entity
from client.sound import Sound


class SoundEntity(Entity):
    def __init__(self, sound: Sound, position: Vector3, class_name: str, propagatable: bool = True, volume: float = 1.0):
        super(SoundEntity, self).__init__(position, class_name)

        self.sound = sound
        self.propagatable = propagatable
        self.volume = volume

    def get_sound(self):
        return self.sound

    def get_volume(self) -> float:
        return self.volume

    def set_volume(self, volume: float):
        self.volume = volume

    def set_propagatable(self, value: bool):
        self.propagatable = value

    def is_propagatable(self):
        """
        Returns True if sound propagates through space i.e. will sound fade out with distance or not, etc.
        """

        return self.propagatable

    def play(self):
        self.sound.play()
