from game.entities.gravity import GravityEntity

class Ball(GravityEntity):
    def __init__(self, size: int = 40, X: int = 600, Y: int = 400) -> None:
        super().__init__(X, Y)
        self.size = size