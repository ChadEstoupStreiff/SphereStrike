from game.entities.movable import MovableEntity
from core import get_env_values

class GravityEntity(MovableEntity):
    def __init__(self, X: int, Y: int, size:int) -> None:
        super().__init__(X, Y, size)

    def apply_gravity(self, time: int):
        self.apply_acceleration(0, -float(get_env_values("GRAVITY")) * time)
