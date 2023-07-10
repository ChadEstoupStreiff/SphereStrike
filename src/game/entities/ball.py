from game.entities import GravityEntity, ColidableEntity
from core import get_env_values

class Ball(ColidableEntity, GravityEntity):
    def __init__(self, X: int = 600, Y: int = 500, size: int = 80) -> None:
        super().__init__(X, Y, size, 10)
        self.last_touch = None

    def respawn(self):
        self.last_touch = None
        self.v_X = 0
        self.v_Y = 50
        self.X = int(get_env_values("TERRAIN_X_SIZE"))/2
        self.Y = int(get_env_values("TERRAIN_Y_SIZE"))/2