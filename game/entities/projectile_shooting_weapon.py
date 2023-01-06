from core.vector3 import Vector3
from game.entities.weapon import Weapon
from game.entities.bullet import Bullet


class ProjectileShootingWeapon(Weapon):
    def __init__(self, bullet: Bullet.__class__, bullet_speed: float, *args, **kwargs):
        super(ProjectileShootingWeapon, self).__init__(*args, **kwargs)
        self.bullet = bullet
        self.bullet_speed = bullet_speed

    def shoot(self, current_position: Vector3):
        if self.bullet_count > 0 and self.current_bullets_in_clip > 0 and self.is_reloaded():
            bullet = self.bullet(current_position, self.damage, self.max_distance, self.bullet_speed)

            self.world.add_entity(bullet)

    def set_state(self, state: dict):
        super(ProjectileShootingWeapon, self).set_state(state)
        self.bullet_speed = state['bullet_speed']
