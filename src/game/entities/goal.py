from game.entities import Player


class Goal:
    def __init__(self, owner: Player, c1x: int, c1y: int, c2x: int, c2y: int) -> None:
        self.owner = owner
        self.c1x = c1x
        self.c1y = c1y
        self.c2x = c2x
        self.c2y = c2y

    def is_inside(self, x: float, y: float, padding: int):
        return (
            x >= min(self.c1x, self.c2x) - padding
            and x <= max(self.c1x, self.c2x) + padding
            and y >= min(self.c1y, self.c2y) - padding
            and y <= max(self.c1y, self.c2y) + padding
        )
