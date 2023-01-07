from core.world import World


class Weapon:
    def __init__(self, world: World, damage: float, recharge_time: int, bullet_count: int, max_bullets_in_clip: int,
                 max_distance: float):
        self.world = world

        self.damage = damage
        self.recharge_time = recharge_time

        self.bullet_count = bullet_count
        self.max_bullets_in_clip = max_bullets_in_clip
        self.current_bullets_in_clip = max_bullets_in_clip

        self.max_distance = max_distance

        self.last_recharge_time = self.world.get_time()

    def shoot(self, *args, **kwargs):
        # Child classes should realise this functionality
        pass

    def set_bullet_count(self, count):
        self.bullet_count = count

    def is_reloaded(self) -> bool:
        if (self.world.get_time() - self.last_recharge_time).seconds <= self.recharge_time:
            return False

        return True

    def recharge(self):
        if self.bullet_count > 0 and self.current_bullets_in_clip < self.max_bullets_in_clip:
            self.last_recharge_time = self.world.get_time()
            if self.current_bullets_in_clip >= self.bullet_count:
                self.current_bullets_in_clip = self.bullet_count
                self.bullet_count = 0
            else:
                self.bullet_count -= self.max_bullets_in_clip

    def get_state(self) -> dict:
        state = {
            'damage': self.damage,
            'recharge_time': self.recharge_time,
            'bullet_count': self.bullet_count,
            'max_bullets_in_clip': self.max_bullets_in_clip,
            'max_distance': self.max_distance,
        }

        return state

    def set_state(self, state: dict):
        self.damage = state.get('damage')
        self.recharge_time = state.get('recharge_time')

        self.bullet_count = state.get('bullet_count')
        self.max_bullets_in_clip = state.get('max_bullets_in_clip')
        self.current_bullets_in_clip = state.get('current_bullets_in_clip')

        self.max_distance = state.get('max_distance')
