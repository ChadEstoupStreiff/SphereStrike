import copy
import logging
import threading
from time import sleep
from typing import List

from core import current_time, get_env_values, is_app_alive
from game.entities.ball import Ball
from game.entities.player import Player


def get_tick_time_length():
    return 1000.0 / int(get_env_values("TPS"))


class GameManager:
    def __init__(self) -> None:
        self.tick = 0

        self.average_last_tick = 0
        self.average_tps = 0

        self.game_thread = None
        self.second_thread = None

        self.players = [Player(X=200), Player(X=1000)]
        self.balls = [Ball()]
        self.players[0].set_velocity(1000, 1000)

    def launch(self):
        self.second_thread = threading.Thread(target=self.second_tick)
        self.second_thread.start()

        self.game_thread = threading.Thread(target=self.game_tick)
        self.game_thread.start()

        self.second_thread.join()
        self.game_thread.join()

    def game_tick(self):
        logging.debug("Starting game_tick tgame hread")
        while is_app_alive():
            start = current_time()

            time_length = int(get_tick_time_length())
            for entity in self.players:
                entity.apply_gravity(time_length)
                entity.move(time_length)

                if entity.X < 0 or entity.X > int(get_env_values("TERRAIN_X_SIZE")):
                    entity.set_coordinates(
                        min(max(0, entity.X), int(get_env_values("TERRAIN_X_SIZE"))),
                        entity.Y
                    )
                    entity.set_velocity(
                        -entity.v_X * float(get_env_values("BOUNCE_PLAYER")),
                        entity.v_Y
                    )
                if entity.Y < 0:
                    entity.set_coordinates(
                        entity.X,
                        0
                    )
                    if entity.v_X > 10 or entity.v_X < -10:
                        entity.set_velocity(
                            entity.v_X*9/10,
                            0
                        )
                    else:
                        entity.set_velocity(
                            0,
                            0
                        )
                elif entity.Y > int(get_env_values("TERRAIN_Y_SIZE")):
                    entity.set_coordinates(
                        entity.X,
                        int(get_env_values("TERRAIN_Y_SIZE"))
                    )
                    entity.set_velocity(
                        entity.v_X,
                        -entity.v_Y * float(get_env_values("BOUNCE_PLAYER"))
                    )

            for entity in self.balls:
                entity.apply_gravity(time_length)
                entity.move(time_length)

                if entity.X < 0 or entity.X > int(get_env_values("TERRAIN_X_SIZE")):
                    entity.set_coordinates(
                        min(max(0, entity.X), int(get_env_values("TERRAIN_X_SIZE"))),
                        entity.Y
                    )
                    entity.set_velocity(
                        -entity.v_X * float(get_env_values("BOUNCE_BALL")),
                        entity.v_Y
                    )
                if entity.Y < 0 or entity.Y > int(get_env_values("TERRAIN_Y_SIZE")):
                    entity.set_coordinates(
                        entity.X,
                        min(max(0, entity.Y), int(get_env_values("TERRAIN_Y_SIZE")))
                    )
                    entity.set_velocity(
                        entity.v_X,
                        -entity.v_Y * float(get_env_values("BOUNCE_BALL"))
                    )

            self.tick += 1
            end = current_time()
            sleep(max(0, (1000.0 / int(get_env_values("TPS")) - end + start) / 1000.0))
        logging.debug("Ending game_tick game thread")

    def second_tick(self):
        logging.debug("Starting second_tick game thread")
        while is_app_alive():
            sleep(1)

            self.average_tps = self.tick - self.average_last_tick
            self.average_last_tick = self.tick

            if self.average_tps < int(get_env_values("TPS")) - 1:
                logging.warning(f"Average TPS: {self.average_tps}")
            else:
                logging.debug(f"Average TPS: {self.average_tps}")
        logging.debug("Ending game_tick game thread")