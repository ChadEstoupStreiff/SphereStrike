from game.entities.gravity import GravityEntity

class PlayerBrain:
    def __init__(self) -> None:
        pass

class Player(GravityEntity):
    def __init__(self, brain: PlayerBrain, size: int = 20, X: int = 600, Y: int = 400) -> None:
        super().__init__(X, Y)
        self.size = size