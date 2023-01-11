from datetime import timedelta
from core.world import World


class Weapon:
    def __init__(self, world: World, damage: float, clip_recharge_time: float, bullet_recharge_time: float, bullet_count: int, max_bullets_in_clip: int,
                 max_distance: float):
        self.world = world

        self.damage = damage
        self.clip_recharge_time = clip_recharge_time
        self.bullet_recharge_time = bullet_recharge_time

        self.bullet_count = bullet_count
        self.max_bullets_in_clip = max_bullets_in_clip
        self.current_bullets_in_clip = max_bullets_in_clip

        self.max_distance = max_distance

        self.next_shot = self.world.get_time()

    def shoot(self, *args, **kwargs):
        # Child classes should realise this functionality
        pass

    def get_bullets_count(self) -> int:
        return self.bullet_count

    def get_bullets_in_clip(self) -> int:
        return self.current_bullets_in_clip

    def set_bullet_count(self, count):
        self.bullet_count = count

    def is_reloaded(self) -> bool:
        if self.next_shot > self.world.get_time():
            return False

        return True

    def is_ready(self) -> bool:
        return self.current_bullets_in_clip > 0 and self.is_reloaded()

    def recharge(self):
        if (self.bullet_count > 0 or self.current_bullets_in_clip > 0) and self.is_reloaded():
            self.next_shot = self.world.get_time() + timedelta(seconds=self.bullet_recharge_time)

            if self.current_bullets_in_clip == 0:
                self.next_shot = self.world.get_time() + timedelta(seconds=self.clip_recharge_time)

                self.current_bullets_in_clip = self.max_bullets_in_clip

                if self.current_bullets_in_clip >= self.bullet_count:
                    self.current_bullets_in_clip = self.bullet_count
                    self.bullet_count = 0
                else:
                    self.bullet_count -= self.max_bullets_in_clip

    def get_state(self) -> dict:
        state = {
            'damage': self.damage,
            'clip_recharge_time': self.clip_recharge_time,
            'bullet_recharge_time': self.bullet_recharge_time,
            'next_shot': self.next_shot.seconds + self.next_shot.microseconds / 1000000,
            'bullet_count': self.bullet_count,
            'current_bullets_in_clip': self.current_bullets_in_clip,
            'max_bullets_in_clip': self.max_bullets_in_clip,
            'max_distance': self.max_distance,
        }

        return state

    def set_state(self, state: dict):
        self.damage = state.get('damage')
        self.clip_recharge_time = state.get('clip_recharge_time')
        self.bullet_recharge_time = state.get('bullet_recharge_time')
        self.next_shot = timedelta(seconds=state.get('next_shot'))

        self.bullet_count = state.get('bullet_count')
        self.max_bullets_in_clip = state.get('max_bullets_in_clip')
        self.current_bullets_in_clip = state.get('current_bullets_in_clip')

        self.max_distance = state.get('max_distance')

    @staticmethod
    def from_state(state: dict, world: World):
        weapon = Weapon(world, 0.0, 0, 0, 0, 0.0)

        weapon.set_state(state)

        return weapon
