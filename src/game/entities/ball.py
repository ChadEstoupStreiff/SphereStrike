from game.entities.gravity import GravityEntity

class Ball(GravityEntity):
    def __init__(self, X: int = 600, Y: int = 500, size: int = 40) -> None:
        super().__init__(X, Y, size)