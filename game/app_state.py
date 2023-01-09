from core.utils.event_emitter import EventEmitter


class AppState:
    """
    Game state container class.\n
    Provides convenient interface to setup settings, watch settings values, etc.
    """

    def __init__(self):
        self.event_emitter = EventEmitter()

        self.volume = 1.0
        self.screen_resolution = (800, 600)

    def get_volume(self) -> float:
        return self.volume

    def get_screen_resolution(self) -> tuple[int]:
        return self.screen_resolution

    def set_volume(self, value: float):
        self.volume = value

        self.event_emitter.emit("volume_changed", value)

    def set_screen_resolution(self, width: int, height: int):
        self.screen_resolution = (width, height)

        self.event_emitter.emit("resolution_changed", width, height)
