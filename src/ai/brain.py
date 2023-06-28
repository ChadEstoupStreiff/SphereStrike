from typing import List

from game.entities.player import PlayerBrain
import random

class RandomBrain(PlayerBrain):
    def get_inputs(self) -> List[bool]:
        inputs = [False, False, False]
        if random.randint(1, 100) <= 5:
            inputs[0] = True
        if random.randint(1, 100) <= 25:
            inputs[1] = True
        if random.randint(1, 100) <= 25:
            inputs[2] = True
        return inputs
