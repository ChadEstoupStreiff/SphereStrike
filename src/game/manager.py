import logging
import threading
from time import sleep
from typing import List

from ai.brain import AIBrain, RandomBrain
from core import current_time, get_env_values, is_app_alive
from game.entities import Ball, Goal, Player


def get_tick_time_length():
    return 1000.0 / int(get_env_values("TPS"))


class GameManager:
    def __init__(self) -> None:
        self.tick_limit = 0
        self.tick = 0

        self.average_last_tick = 0
        self.average_tps = 0

        self.game_thread = None
        self.second_thread = None

        self.players = [
            Player(brain=AIBrain(), color="green"),
            Player(brain=AIBrain(), color="purple"),
        ]
        self.balls = [Ball()]
        self.goals = [
            Goal(self.players[0], 0, 0, 40, 300),
            Goal(
                self.players[1],
                int(get_env_values("TERRAIN_X_SIZE")),
                0,
                int(get_env_values("TERRAIN_X_SIZE")) - 40,
                300,
            ),
        ]

        self.reset()

    def reset(self):
        self.tick = 0

        self.average_last_tick = 0
        self.average_tps = 0

        self.game_thread = None
        self.second_thread = None

        for ball in self.balls:
            ball.respawn()
        for index, player in enumerate(self.players):
            player.points = 0
            player.v_X = 0
            player.v_Y = 0
            player.X = index * 1000 % int(get_env_values("TERRAIN_X_SIZE")) + 250
            player.Y = 0


    def launch(self, second_tick=False):
        if second_tick:
            self.second_thread = threading.Thread(target=self.second_tick)
            self.second_thread.start()

        self.game_thread = threading.Thread(target=self.game_tick)
        self.game_thread.start()

        if second_tick:
            self.second_thread.join()
        self.game_thread.join()

    def game_tick(self):
        logging.debug("Starting game_tick tgame hread")
        while (self.tick_limit > 0 and self.tick < self.tick_limit) or (
            self.tick_limit <= 0 and is_app_alive()
        ):
            if float(get_env_values("TPS_SPEED")) > 0:
                start = current_time()

                self.check_colisions()

                self.move_entities()

                self.check_goals()

                self.tick += 1
                end = current_time()
                if float(get_env_values("TPS_SPEED")) > 0:
                    sleep(
                        max(
                            0,
                            (1000.0 / int(get_env_values("TPS")) - end + start)
                            / 1000.0,
                        )
                        / float(get_env_values("TPS_SPEED"))
                    )
        logging.debug("Ending game_tick game thread")

    def check_colisions(self):
        # players to players
        for i in range(len(self.players) - 1):
            for j in range(i + 1, len(self.players)):
                self.players[i].check_colision(self.players[j])

        # balls to balls
        for i in range(len(self.balls) - 1):
            for j in range(i + 1, len(self.balls)):
                self.balls[i].check_colision(self.balls[j])

        # player to ball
        for player in self.players:
            for ball in self.balls:
                if ball.check_colision(player):
                    ball.last_touch = player

    def move_entities(self):
        time_length = int(get_tick_time_length())

        for entity in self.players:
            entity.apply_gravity(time_length)
            entity.move(time_length, self)

            if (
                entity.X < entity.size
                or entity.X > int(get_env_values("TERRAIN_X_SIZE")) - entity.size
            ):
                entity.set_coordinates(
                    min(
                        max(entity.size, entity.X),
                        int(get_env_values("TERRAIN_X_SIZE")) - entity.size,
                    ),
                    entity.Y,
                )

                if entity.Y < entity.size:
                    entity.set_velocity(0, entity.v_Y)
                else:
                    entity.set_velocity(
                        -entity.v_X * float(get_env_values("BOUNCE_PLAYER")),
                        entity.v_Y,
                    )
            if entity.Y < entity.size:
                entity.set_coordinates(entity.X, entity.size)
                if entity.v_X > 10 or entity.v_X < -10:
                    entity.set_velocity(entity.v_X * 9 / 10, 0)
                else:
                    entity.set_velocity(0, 0)
            elif entity.Y > int(get_env_values("TERRAIN_Y_SIZE")) - entity.size:
                entity.set_coordinates(
                    entity.X,
                    int(get_env_values("TERRAIN_Y_SIZE")) - entity.size,
                )
                entity.set_velocity(
                    entity.v_X,
                    -entity.v_Y * float(get_env_values("BOUNCE_PLAYER")),
                )

        for entity in self.balls:
            entity.apply_gravity(time_length)
            entity.move(time_length)

            if (
                entity.X < entity.size
                or entity.X > int(get_env_values("TERRAIN_X_SIZE")) - entity.size
            ):
                entity.set_coordinates(
                    min(
                        max(entity.size, entity.X),
                        int(get_env_values("TERRAIN_X_SIZE")) - entity.size,
                    ),
                    entity.Y,
                )
                entity.set_velocity(
                    -entity.v_X * float(get_env_values("BOUNCE_BALL")),
                    entity.v_Y,
                )
            if (
                entity.Y < entity.size
                or entity.Y > int(get_env_values("TERRAIN_Y_SIZE")) - entity.size
            ):
                entity.set_coordinates(
                    entity.X,
                    min(
                        max(entity.size, entity.Y),
                        int(get_env_values("TERRAIN_Y_SIZE")) - entity.size,
                    ),
                )
                entity.set_velocity(
                    entity.v_X,
                    -entity.v_Y * float(get_env_values("BOUNCE_BALL")),
                )

    def check_goals(self):
        for goal in self.goals:
            for ball in self.balls:
                if goal.is_inside(ball.X, ball.Y, ball.size / 2):
                    ball.last_touch.points += 10
                    ball.respawn()

    def second_tick(self):
        logging.debug("Starting second_tick game thread")
        while (self.tick_limit > 0 and self.tick < self.tick_limit) or (
            self.tick_limit <= 0 and is_app_alive()
        ):
            sleep(1)

            self.average_tps = self.tick - self.average_last_tick
            self.average_last_tick = self.tick

            if self.average_tps < int(get_env_values("TPS")) * 0.9:
                logging.warning(f"Average TPS: {self.average_tps}")
            else:
                logging.debug(f"Average TPS: {self.average_tps}")
        logging.debug("Ending game_tick game thread")
