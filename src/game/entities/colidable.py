import logging
import math

from core import get_env_values
from game.entities import MovableEntity


class ColidableEntity(MovableEntity):
    def __init__(self, X: int, Y: int, size: int, weight: int = 50) -> None:
        super().__init__(X, Y, size)
        self.weight = weight

    def check_colision(self, entity):
        distance = math.sqrt((self.X - entity.X) ** 2 + (self.Y - entity.Y) ** 2)
        sizes = self.size + entity.size
        if distance < sizes:
            if distance != 0:
                # normalized direction vector
                v_X = abs(entity.X - self.X) / distance
                v_Y = abs(entity.Y - self.Y) / distance

                # replace
                self.set_coordinates(
                    self.X - v_X * (sizes - distance),
                    self.Y - v_Y * (sizes - distance),
                )
                entity.set_coordinates(
                    entity.X + v_X * (sizes - distance),
                    entity.Y + v_Y * (sizes - distance),
                )

                # Scalar product
                u = (self.v_X, self.v_Y)
                v = (entity.X - self.X, entity.Y - self.Y)

                v_m = math.sqrt(v[0] ** 2 + v[1] ** 2)
                v_u = (u[0] / v_m, u[1] / v_m)

                ps = u[0] * v_u[0] + u[1] * v_u[1]

                proj_u = (ps * v_u[0], ps * v_u[1])

                # acceleration
                # logging.debug(proj_u)
                entity.apply_acceleration(
                    float(get_env_values("COLISION"))/1000000000000 * self.weight * proj_u[0],
                    float(get_env_values("COLISION"))/1000000000000 * self.weight * proj_u[1],
                )

                # Scalar product
                u = (entity.v_X, entity.v_Y)
                v = (self.X - entity.X, self.Y - entity.Y)

                v_m = math.sqrt(v[0] ** 2 + v[1] ** 2)
                v_u = (u[0] / v_m, u[1] / v_m)

                ps = u[0] * v_u[0] + u[1] * v_u[1]

                proj_u = (ps * v_u[0], ps * v_u[1])

                # acceleration
                self.apply_acceleration(
                    float(get_env_values("COLISION"))/1000000000000 * entity.weight * proj_u[0],
                    float(get_env_values("COLISION"))/1000000000000 * entity.weight * proj_u[1],
                )
