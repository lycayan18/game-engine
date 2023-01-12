from client.sound_modules.pygame.pygame_sound_module import PygameSound
from game.client.assets.assets import Assets


def setup_background_sounds():
    background = Assets.sounds.star_ship_engine_sfx

    background.set_repeatable(True)

    background.play()
