from core.entity import Entity
from core.vector3 import Vector3
from core.world import World
from game.entities.star_ship import StarShip
from game.lib.rotation_to_direction import rotation_to_direction


class Bullet(Entity):
    def __init__(self, world: World, owner: int, start_position: Vector3, rotation: Vector3, damage: float,
                 max_distance: float, speed: float):
        super(Bullet, self).__init__(start_position, 'bullet')

        self.world = world
        self.owner = owner
        self.start_position = start_position
        self.prev_position = start_position
        self.rotation = rotation or Vector3(0, 0, 0)
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

        self.position += direction * Vector3(self.speed)

    def collision_check(self, star_ship: StarShip):
        collision_model = star_ship.get_collision_model()

        if (collision_model.line_intersection(self.prev_position, self.position) is not None and
                star_ship.id != self.owner):
            star_ship.damage(self.damage)

    def get_state(self):
        return {
            **super(Bullet, self).get_state(),
            "rotation": {
                "x": self.rotation.x,
                "y": self.rotation.y,
                "z": self.rotation.z,
            },
            "owner": self.owner,
            "speed": self.speed,
            "max_distance": self.max_distance,
            "damage": self.damage,
            "prev_position": {
                "x": self.prev_position.x,
                "y": self.prev_position.y,
                "z": self.prev_position.z,
            },
            "start_position": {
                "x": self.start_position.x,
                "y": self.start_position.y,
                "z": self.start_position.z,
            }
        }

    def set_state(self, state: dict):
        super(Bullet, self).set_state(state)

        # To prevent link lost
        self.rotation.x = state["rotation"]["x"]
        self.rotation.y = state["rotation"]["y"]
        self.rotation.z = state["rotation"]["z"]

        self.owner = state["owner"]

        self.speed = state["speed"]
        self.damage = state["damage"]
        self.max_distance = state["max_distance"]
        self.prev_position = Vector3(**state["prev_position"])
        self.start_position = Vector3(**state["start_position"])

    def think(self):
        self.move()
        self.calculate_distance()

        for entity in self.world.entities:
            if isinstance(entity, StarShip):
                self.collision_check(entity)

    @staticmethod
    def from_state(state: dict, world: World = None):
        bullet = Bullet(world, 0, None, None, None, None, None)

        bullet.set_state(state)

        return bullet
