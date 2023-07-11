import copy
import json
import logging
import os
import signal
import sys
import threading

from tqdm import tqdm

from core import get_env_values
from core.utils import set_app_alive, set_env_value
from game import GameManager
from game.entities import Player


def signal_handler(sig, frame):
    TrainManager().stop()


class TrainManager:
    __instance = None

    @staticmethod
    def __new__(cls, *args, **kwargs):
        if TrainManager.__instance is None:
            TrainManager.__instance = super(TrainManager, cls).__new__(
                cls, *args, **kwargs
            )

            TrainManager.games = None
            TrainManager.games_threads = None
            TrainManager.model_info = {}
        return TrainManager.__instance

    def start(self):
        logging.root.setLevel(get_env_values("LOG_LEVEL"))
        logging.info("Setup ...")
        signal.signal(signal.SIGINT, signal_handler)
        logging.info("Env values:")
        for key, value in get_env_values().items():
            logging.info(f"  - {key}: {value}")

        set_env_value("TPS_SPEED", sys.float_info.max)
        tick_limit = int(get_env_values("TRAIN_GAME_LENGTH"))
        self.games = []
        for _ in tqdm(range(int(get_env_values("TRAIN_NBR_GAMES")))):
            self.games.append(GameManager())
        for game in self.games:
            game.tick_limit = tick_limit

        logging.info("Starting training...")

        for i in range(1, int(get_env_values("TRAIN_ITERATION")) + 1):
            logging.info(f"=========== ITERATION {i} ===========")

            # PLAY
            logging.info("Playing...")
            self.games_threads = []
            for game in self.games:
                game.reset()
                self.games_threads.append(threading.Thread(target=game.launch))

            for game_thread in self.games_threads:
                game_thread.start()

            for game_thread in self.games_threads:
                game_thread.join()

            # SELECT
            logging.info("Selecting...")
            players = self.sort_players()
            players = players[
                : int(len(players) * float(get_env_values("TRAIN_SELECTION_RATE")))
            ]

            if i % int(get_env_values("TRAIN_SAVE_PERIOD")) == 0:
                self.save_model(model_name=f"step_{i}")

            logging.info("Reproducing...")
            for i in range(int(get_env_values("TRAIN_NBR_GAMES")) * 2 - len(players)):
                players.append(Player(brain=copy.deepcopy(players[i].brain)))
            for i, game in enumerate(self.games):
                game.players = [
                    players[i * 2],
                    players[i * 2 + 1],
                ]

            # TODO MUTATE
            logging.info("Mutating...")
            for player in players:
                pass

        logging.info("Stopped")

    def sort_players(self):
        players = []
        for game in self.games:
            players.extend(game.players)
        players.sort(key=lambda p: p.points, reverse=True)
        return players

    def save_model(self, model_name: str = "latest"):
        model_folder = os.path.join(
            get_env_values("MODEL_PATH"), get_env_values("MODEL_NAME")
        )
        if not os.path.exists(model_folder):
            os.makedirs(model_folder)
        with open(os.path.join(model_folder, f"{model_name}.json"), "w") as f_o:
            f_o.write(json.dumps(self.model_info))
        self.model_info
        self.sort_players()[0].save_model(model_name=f"{model_name}.cpkt")

    def stop(self):
        logging.info("Stopping...")
        self.save_model()
        set_app_alive(False)


def main():
    TrainManager().start()


if __name__ == "__main__":
    main()
