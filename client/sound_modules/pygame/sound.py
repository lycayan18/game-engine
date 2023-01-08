import pygame
from client.sound import Sound


class PygameSound(Sound):
    def __init__(self, sound: pygame.mixer.Sound):
        super(PygameSound, self).__init__()

        self.sound = sound
        self.current_channel = None

    def play(self):
        super(PygameSound, self).play()

        self.current_channel = self.sound.play(-1 if self.repeatable else 0)

    def stop(self):
        self.event_emitter.emit("stop")

        self.current_channel.stop()

    def set_volume(self, left: float, right: float):
        if self.current_channel:
            self.current_channel.set_volume(left, right)

    def set_repeatable(self, value: bool):
        self.repeatable = value

    def check_for_end(self):
        if self.current_channel:
            if not self.current_channel.get_busy():
                if self.repeatable:
                    self.current_channel.play()
                else:
                    self.current_channel = None

                self.event_emitter.emit("end")
