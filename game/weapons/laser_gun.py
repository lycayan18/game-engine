from core.world import World
from game.weapons.projectile_shooting_weapon import ProjectileShootingWeapon
from game.entities.bullet import Bullet


class LaserGun(ProjectileShootingWeapon):
    def __init__(self, world: World):
        damage = 10
        recharge_time = 4
        bullet_speed = 500
        bullet_count = 500
        max_bullets_in_clip = 50
        max_distance = 2000

        super(LaserGun, self).__init__(world=world, bullet=Bullet, damage=damage, recharge_time=recharge_time,
                                       bullet_count=bullet_count, bullet_speed=bullet_speed,
                                       max_bullets_in_clip=max_bullets_in_clip,
                                       max_distance=max_distance)