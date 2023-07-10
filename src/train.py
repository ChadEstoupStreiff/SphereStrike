import logging
import signal
import threading

from core import get_env_values
from core.utils import set_app_alive, set_env_value
from game import GameManager
import sys


def signal_handler(sig, frame):
    TrainManager().stop()


class TrainManager:
    __instance = None

    @staticmethod
    def __new__(cls, *args, **kwargs):
        if TrainManager.__instance is None:
            TrainManager.__instance = super(TrainManager, cls).__new__(cls, *args, **kwargs)

            TrainManager.games = None
            TrainManager.games_threads = None
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
        self.games = [GameManager() for _ in range(len(get_env_values("TRAIN_NBR_GAMES")))]
        for game in self.games:
            game.tick_limit = tick_limit

        logging.info("Starting training...")

        for i in range(len(get_env_values("TRAIN_ITERATION"))):
            logging.info(f"ITERATION {i} ...")

            # PLAY
            self.games_threads = []
            for game in self.games:
                self.games_threads.append(threading.Thread(target=game.launch))

            for game_thread in self.games_threads:
                game_thread.start()

            logging.info("Started !")
            for game_thread in self.games_threads:
                game_thread.join()

            # TODO SELECT
            # TODO REPRODUCE
            # TODO MUTATE


        logging.info("Stopped")

    def stop(self):
        logging.info("Stopping...")
        set_app_alive(False)


def main():
    TrainManager().start()


if __name__ == "__main__":
    main()
