from core.entities.player import Player


class ShootingEntity(Player):
    def __init__(self, weapon, *args, **kwargs):
        super(ShootingEntity, self).__init__(*args, **kwargs)
        self.weapon = weapon

    def set_weapon(self, weapon):
        self.weapon = weapon

    def shoot(self):
        self.weapon.shoot()
