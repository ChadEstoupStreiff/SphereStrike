import math
import numpy as np

from core import get_env_values
from game.entities import MovableEntity


class ColidableEntity(MovableEntity):
    def __init__(self, X: int, Y: int, size: int, weight: int = 50) -> None:
        super().__init__(X, Y, size)
        self.weight = weight

    def check_colision(self, entity, time: int):
        distance = math.sqrt((self.X - entity.X) ** 2 + (self.Y - entity.Y) ** 2)
        sizes = self.size + entity.size
        if distance < sizes:
            if distance != 0:

                vA_final, vB_final = calculate_final_velocities(
                    [self.X, self.Y],
                    [self.v_X, self.v_Y],
                    self.weight,
                    [entity.X, self.Y],
                    [entity.v_X, entity.v_Y],
                    entity.weight,
                )

                self.set_velocity(vA_final[0], vA_final[1])
                entity.set_velocity(vB_final[0], vB_final[1])

                # normalized direction vector
                v_X = (entity.X - self.X) / distance
                v_Y = (entity.Y - self.Y) / distance

                # replace
                self.set_coordinates(
                    self.X - v_X * (sizes - distance),
                    self.Y - v_Y * (sizes - distance),
                )
                entity.set_coordinates(
                    entity.X + v_X * (sizes - distance),
                    entity.Y + v_Y * (sizes - distance),
                )

def calculate_final_velocities(pA, vA, m_A, pB, vB, m_B):
    pA = np.array(pA)
    pB = np.array(pB)
    vA = np.array(vA)
    vB = np.array(vB)

    d = pB - pA
    d = d / np.linalg.norm(d)

    vA_parallel = np.dot(vA, d) * d
    vA_perpendicular = vA - vA_parallel
    vB_parallel = np.dot(vB, d) * d
    vB_perpendicular = vB - vB_parallel

    vA_final = (vA_parallel * (m_A - m_B) + 2 * m_B * vB_parallel) / (m_A + m_B) + vA_perpendicular
    vB_final = (vB_parallel * (m_B - m_A) + 2 * m_A * vA_parallel) / (m_A + m_B) + vB_perpendicular

    return vA_final, vB_final
