from core.entities.viewable_entity import ViewableEntity
from core.vector3 import Vector3


class Bullet(ViewableEntity):
    def __init__(self, start_position: Vector3, damage: float, max_distance: float, speed: float):
        super(Bullet, self).__init__('bullet', start_position)
        self.start_position = start_position
        self.damage = damage
        self.max_distance = max_distance
        self.speed = speed

    def calculate_distance(self):
        distance = self.start_position.calculate_distance(self.position)
        if distance > self.max_distance:
            self.delete()

    def move(self):
        ...

    def collision_check(self):
        ...

    def update(self):
        self.move()
        self.calculate_distance()
        self.collision_check()
