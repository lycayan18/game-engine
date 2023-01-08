from core.utils.event_emitter import EventEmitter


class Sound:
    """Base class for all sounds"""

    def __init__(self):
        self.event_emitter = EventEmitter()
        self.repeatable = False

    def play(self):
        self.event_emitter.emit("play")

    def stop(self):
        self.event_emitter.emit("stop")

    def set_repeatable(self, value: bool):
        self.repeatable = value
