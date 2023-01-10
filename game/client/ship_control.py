from math import pi

import pygame

from core.vector3 import Vector3
from client.camera import Camera
from game.client.entities.client_star_ship import ClientStarShip
from game.utils.keyboard_control_manager import KeyboardControlManager
from game.client.app_state import AppState

MIN_SPEED = 300
MAX_SPEED = 600
ACCELERATION = 100 / 60  # Divide by FPS to make it acceleration per second
# Divide by FPS to make it acceleration per second
ANGLE_MOUSE_ACCELERATION = 180 * pi / 180 / 60


def update_camera_position(camera: Camera, player: ClientStarShip):
    pass


def ship_control(controls_manager: KeyboardControlManager):
    width, height = pygame.display.get_window_size()

    player: ClientStarShip = AppState.get_current_player_entity()

    if controls_manager.is_active("forward"):
        player.set_speed(min(MAX_SPEED, player.get_speed() + ACCELERATION))

    if controls_manager.is_active("backward"):
        player.set_speed(max(MIN_SPEED, player.get_speed() - ACCELERATION))

    # Rotate ship by mouse

    # Get mouse movement
    x, y = pygame.mouse.get_pos()

    # Convert pixel coordinates to screen coordinates [-1; 1]
    x = x / width * 2.0 - 1.0
    y = y / height * 2.0 - 1.0

    # Cursor position back to screen center
    pygame.mouse.set_pos(width / 2, height / 2)

    delta_rotation = Vector3(x * ANGLE_MOUSE_ACCELERATION,
                             y * ANGLE_MOUSE_ACCELERATION,
                             0.0)

    player.set_rotation(player.get_rotation() + delta_rotation)

    # Check for shooting
    if controls_manager.is_active("shoot") or pygame.mouse.get_pressed()[0]:
        player.shoot()

    update_camera_position()
