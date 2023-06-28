import math

class MovableEntity:
    def __init__(self, X: int, Y: int, size: int) -> None:
        self.size = size
        self.set_coordinates(X, Y)
        self.set_velocity(0, 0)

    def move(self, time: int):
        self.X = self.X + self.v_X * time/1000.
        self.Y = self.Y + self.v_Y * time/1000.

    def set_coordinates(self, X: int, Y: int):
        self.X = X
        self.Y = Y
    def set_velocity(self, X: int, Y: int):
        self.v_X = X
        self.v_Y = Y

    def apply_acceleration(self, X: int, Y: int):
        self.v_X = self.v_X + X
        self.v_Y = self.v_Y + Y

    def get_speed(self):
        return math.sqrt(self.v_X*self.v_X + self.v_Y*self.v_Y)
