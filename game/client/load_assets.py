"""
All assets should be loaded here
"""

import pygame
from client.sound_modules.pygame.sound import PygameSound
from game.client.assets.assets import Assets


def load_assets():
    # **********************************************
    # *                  LOAD SFX                  *
    # **********************************************

    # Laser gun
    Assets.sounds.laser_gun_shot = PygameSound(pygame.mixer.Sound(
        "./game/client/assets/sounds/weapons/lasergun/laser_gun_fire.wav"
    ))

    # Ship background
    Assets.sounds.star_ship_engine_sfx = PygameSound(pygame.mixer.Sound(
        "./game/client/assets/sounds/ship_bg.wav"
    ))

    # Space engine
    Assets.sounds.space_engine_sfx = PygameSound(pygame.mixer.Sound(
        "./game/client/assets/sounds/space_engine.wav"
    ))
