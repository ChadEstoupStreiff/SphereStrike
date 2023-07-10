from abc import ABC, abstractmethod
from typing import List

from core import get_env_values
from game.entities import ColidableEntity, GravityEntity


class PlayerBrain(ABC):
    @abstractmethod
    def get_inputs(self, game) -> List[bool]:
        # [JUMP, LEFT, RIGHT]
        raise NotImplementedError


class KeyBoardBrain(PlayerBrain):
    def __init__(self, root) -> None:
        super().__init__()

        self.jump = False
        self.left = False
        self.right = False

        root.bind("<KeyPress>", self.key_press)
        root.bind("<KeyRelease>", self.key_released)

    def key_press(self, e):
        if e.keysym == "z":
            self.jump = True
        elif e.keysym == "a":
            self.left = True
        elif e.keysym == "e":
            self.right = True

    def key_released(self, e):
        if e.keysym == "z":
            self.jump = False
        elif e.keysym == "a":
            self.left = False
        elif e.keysym == "e":
            self.right = False

    def get_inputs(self, _) -> List[bool]:
        inputs = [self.jump, self.left, self.right]
        self.jump = False
        return inputs


class Player(ColidableEntity, GravityEntity):
    def __init__(
        self,
        color: str = "yellow",
        size: int = 20,
        X: int = 600,
        Y: int = 400,
        brain: PlayerBrain = None,
    ) -> None:
        super().__init__(X, Y, size, 30)
        self.color = color
        self.points = 0
        self.brain = brain
        self.double_jump = True

    def move(self, time: int, game):
        if self.brain is not None:
            inputs = self.brain.get_inputs(game)

            if self.Y == self.size:
                if inputs[0]:
                    self.double_jump = True
                    self.set_velocity(
                        self.v_X, int(get_env_values("PLAYER_JUMP_HEIGHT"))
                    )
                if inputs[1] and not inputs[2]:
                    self.set_velocity(
                        -int(get_env_values("PLAYER_GROUND_SPEED")), self.v_Y
                    )
                elif not inputs[1] and inputs[2]:
                    self.set_velocity(
                        int(get_env_values("PLAYER_GROUND_SPEED")), self.v_Y
                    )
            else:
                if inputs[0] and self.double_jump:
                    self.double_jump = False
                    self.set_velocity(
                        self.v_X, int(get_env_values("PLAYER_JUMP_HEIGHT"))
                    )
                if inputs[1] and not inputs[2]:
                    if self.v_X > -int(get_env_values("PLAYER_AIR_CONTROL")) * 35:
                        self.apply_acceleration(
                            -int(get_env_values("PLAYER_AIR_CONTROL")), 0
                        )
                elif not inputs[1] and inputs[2]:
                    if self.v_X < int(get_env_values("PLAYER_AIR_CONTROL")) * 35:
                        self.apply_acceleration(
                            int(get_env_values("PLAYER_AIR_CONTROL")), 0
                        )

        super().move(time)
