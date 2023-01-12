from core.vector3 import Vector3
from game.weapons.weapon import Weapon
from game.entities.bullet import Bullet


class ProjectileShootingWeapon(Weapon):
    def __init__(self, bullet: Bullet.__class__, bullet_speed: float, *args, **kwargs):
        super(ProjectileShootingWeapon, self).__init__(*args, **kwargs)
        self.bullet = bullet
        self.bullet_speed = bullet_speed

    def shoot(self, current_position: Vector3, rotation: Vector3):
        if self.is_ready():
            bullet = self.bullet(self.world, self.owner, current_position, rotation, self.damage, self.max_distance,
                                 self.bullet_speed)

            self.world.add_entity(bullet)

            self.current_bullets_in_clip -= 1

            self.recharge()

            return True

    def get_state(self) -> dict:
        state = {
            **super(ProjectileShootingWeapon, self).get_state(),
            "bullet_speed": self.bullet_speed
        }

        return state

    def set_state(self, state: dict):
        super(ProjectileShootingWeapon, self).set_state(state)

        self.bullet_speed = state['bullet_speed']
