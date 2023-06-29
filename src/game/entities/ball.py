from game.entities import GravityEntity, ColidableEntity

class Ball(ColidableEntity, GravityEntity):
    def __init__(self, X: int = 600, Y: int = 500, size: int = 80) -> None:
        super().__init__(X, Y, size, 10)