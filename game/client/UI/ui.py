import pygame
from client.renderers.opengl.opengl_renderer import OpenGLRenderer
from client.texture2d import Texture2D
from game.client.app_state import AppState

surface: pygame.Surface = None
ui_texture: Texture2D = None


def init_ui(renderer: OpenGLRenderer, width: int, height: int):
    global surface
    global ui_texture

    ui_texture = Texture2D(width * 0.5, height * 0.5, AppState.get_engine())

    surface = pygame.Surface((width * 0.5, height * 0.5), pygame.SRCALPHA, 32)

    ui_texture.load_from_data(pygame.image.tostring(surface, "RGBA", True))

    renderer.set_ui_texture(ui_texture)


def draw_ui():
    player = AppState.get_current_player_entity()

    text_surface = pygame.font.Font(None, 32).render(
        f"Health: {player.get_health()}", True, (255, 255, 255, 255), (0, 0, 0, 0))

    surface.blit(text_surface, (0, 0))

    ui_texture.load_from_data(pygame.image.tostring(
        surface.convert_alpha(), "RGBA", True))
    ui_texture.update()
