from core.world import World
from game.weapons.projectile_shooting_weapon import ProjectileShootingWeapon
from game.entities.bullet import Bullet


class LaserGun(ProjectileShootingWeapon):
    def __init__(self, world: World):
        damage = 10
        bullet_recharge_time = 0.1
        clip_recharge_time = 3
        bullet_speed = 0.1
        bullet_count = 500
        max_bullets_in_clip = 50
        max_distance = 100

        super(LaserGun, self).__init__(world=world, bullet=Bullet, damage=damage,
                                       bullet_recharge_time=bullet_recharge_time,
                                       clip_recharge_time=clip_recharge_time,
                                       bullet_count=bullet_count, bullet_speed=bullet_speed,
                                       max_bullets_in_clip=max_bullets_in_clip,
                                       max_distance=max_distance)

    @staticmethod
    def from_state(state: dict, world: World):
        weapon = LaserGun(world)

        weapon.set_state(state)

        return weapon
