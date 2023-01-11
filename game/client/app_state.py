from core.utils.event_emitter import EventEmitter
from core.entities.player import Player
from core.world import World
from client.camera import Camera


class AppState:
    """
    Game state container class.\n
    Provides convenient interface to setup settings, watch settings values, etc.
    """
    volume = 1.0
    fps = 60.0
    screen_resolution = (800, 600)
    current_player_entity = None
    camera = None
    world = None
    event_emitter = EventEmitter()

    @staticmethod
    def set_world(world: World):
        AppState.world = world

        AppState.event_emitter.emit("world_changed", world)

    @staticmethod
    def get_world() -> World:
        return AppState.world

    @staticmethod
    def set_camera(camera: Camera):
        AppState.camera = camera

        AppState.event_emitter.emit("camera_changed", camera)

    @staticmethod
    def get_camera() -> Camera:
        return AppState.camera

    @staticmethod
    def set_volume(value: float):
        AppState.volume = value

        AppState.event_emitter.emit("volume_changed", value)

    @staticmethod
    def get_volume() -> float:
        return AppState.volume

    @staticmethod
    def set_fps(value: float):
        AppState.fps = value

        AppState.event_emitter.emit("fps_changed", value)

    @staticmethod
    def get_fps() -> float:
        return AppState.fps

    @staticmethod
    def set_screen_resolution(width: int, height: int):
        AppState.screen_resolution = (width, height)

        AppState.event_emitter.emit("resolution_changed", width, height)

    @staticmethod
    def get_screen_resolution() -> tuple[int]:
        return AppState.screen_resolution

    @staticmethod
    def set_current_player_entity(entity: Player):
        AppState.current_player_entity = entity

        AppState.event_emitter.emit("current_player_entity_changed", entity)

    @staticmethod
    def get_current_player_entity() -> Player:
        return AppState.current_player_entity
