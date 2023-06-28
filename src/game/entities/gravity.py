from game.entities.movable import MovableEntity


class GravityEntity(MovableEntity):
    __g = 9.8 / 10

    def __init__(self, X: int, Y: int) -> None:
        super().__init__(X, Y)

    def apply_gravity(self, time: int):
        self.apply_acceleration(0, -GravityEntity.__g * time)
