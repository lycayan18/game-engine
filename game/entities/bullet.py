from core.entity import Entity
from core.vector3 import Vector3
from core.world import World
from game.entities.star_ship import StarShip
from game.lib.rotation_to_direction import rotation_to_direction


class Bullet(Entity):
    def __init__(self, world: World, start_position: Vector3, rotation: Vector3, damage: float,
                 max_distance: float, speed: float):
        super(Bullet, self).__init__(start_position, 'bullet')

        self.world = world
        self.start_position = start_position
        self.prev_position = start_position
        self.rotation = rotation
        self.damage = damage
        self.max_distance = max_distance
        self.speed = speed

    def calculate_distance(self):
        distance = self.start_position.calculate_distance(self.position)
        if distance > self.max_distance:
            self.delete()

    def move(self):
        self.prev_position = self.position.copy()

        direction = rotation_to_direction(self.rotation)
        self.position += direction * self.speed
        self.push_event({
            "type": "bullet_move",
            "position": {
                "x": self.position.x,
                "y": self.position.y,
                "z": self.position.z
            }
        })

    def collision_check(self, star_ship: StarShip):
        if star_ship.get_collision_model().line_intersection(self.prev_position, self.position) is not None:
            star_ship.damage(self.damage)

    def think(self):
        self.move()
        self.calculate_distance()

        for entity in self.world.entities:
            if isinstance(entity, StarShip):
                self.collision_check(entity)

    @staticmethod
    def from_state(state: dict):
        return Bullet.set_state(state)