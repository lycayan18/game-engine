import sys
import pygame
from client.sound_modules.pygame.pygame_sound_module import PygameSoundModule
from game.app_state import AppState
from game.constants.registry_associations import CLIENT_REGISTRY_ASSOCIATIONS
from client.camera import Camera
from client.renderers.opengl.opengl_renderer import OpenGLRenderer
from game.client.client import Client
from core.world import World
from core.registry import Registry
from game.utils.keyboard_control_manager import KeyboardControlManager

controls_manager = KeyboardControlManager()

# ********************************************************
# *                    INITIALIZATION                    *
# ********************************************************


def init_modules(engine: Client):
    # Init graphcis subsystem

    pygame.init()
    pygame.font.init()
    pygame.display.gl_get_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_get_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK,
                                    pygame.GL_CONTEXT_PROFILE_CORE)
    pygame.display.set_mode(AppState.get_screen_resolution(),
                            flags=pygame.OPENGL | pygame.DOUBLEBUF)

    renderer = OpenGLRenderer(*AppState.get_screen_resolution(), Camera())

    engine.add_module(renderer)

    # Init sound subsystem

    pygame.mixer.init()

    sound_module = PygameSoundModule(renderer.get_camera())

    engine.add_module(sound_module)


# ********************************************************
# *                       ROUTINES                       *
# ********************************************************


def update_all(world: World, engine: Client):
    engine.request_current_entity_id()
    engine.send_world_state_request()
    engine.send_pull_events_request()
    engine.send_events()

    AppState.set_current_player_entity(
        world.get_entity_by_id(engine.get_current_entity_id())
    )


def run_basic_routine():
    """
    Runs basic routines that MUST run every tick, such as checking for window close.
    """

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def wait_for_client_authorize(engine: Client):
    """
    Requests client id and waits till it gets it.
    """

    engine.request_client_id()

    while not engine.is_authorized():
        engine.tick()

        # Let user at least close the window while waiting
        run_basic_routine()


def wait_for_current_player_entity(engine: Client):
    """
    Requests current player entity id and waits till it gets it.
    """

    engine.request_current_entity_id()

    while engine.get_current_entity_id() == -1:
        engine.tick()

        # Let user at least close the window while waiting
        run_basic_routine()


def main(ip: str, port: int):
    # *****************************
    # * Initialize everything
    # *****************************

    # Initialize controls

    controls_manager.bind_key(pygame.K_w, 'forward')
    controls_manager.bind_key(pygame.K_s, 'backward')

    # Initialize engine, world, modules, etc.

    world = World(Registry(CLIENT_REGISTRY_ASSOCIATIONS))
    engine = Client(world, ip, port)

    AppState.set_world(world)

    init_modules(engine)

    wait_for_client_authorize(engine)
    wait_for_current_player_entity(engine)

    AppState.set_current_player_entity(
        world.get_entity_by_id(engine.get_current_entity_id())
    )

    while True:
        engine.tick()

        update_all(engine)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                controls_manager.handle_key_down(event.key)
            elif event.type == pygame.KEYUP:
                controls_manager.handle_key_up(event.key)
