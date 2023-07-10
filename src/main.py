import logging
import signal
import threading

from core import get_env_values
from core.utils import set_app_alive
from game import GameManager
from graphics import GameUI


def signal_handler(sig, frame):
    AppManager().stop()


class AppManager:
    __instance = None

    @staticmethod
    def __new__(cls, *args, **kwargs):
        if AppManager.__instance is None:
            AppManager.__instance = super(AppManager, cls).__new__(cls, *args, **kwargs)

            AppManager.game = None
            AppManager.game_thread = None
        return AppManager.__instance

    def start(self):
        logging.root.setLevel(get_env_values("LOG_LEVEL"))
        logging.info("Setup ...")
        signal.signal(signal.SIGINT, signal_handler)
        logging.info("Env values:")
        for key, value in get_env_values().items():
            logging.info(f"  - {key}: {value}")
        self.game = GameManager()

        logging.info("Starting game...")
        self.game_thread = threading.Thread(target=self.game.launch)

        self.ui = GameUI(self.game)
        self.ui_thread = threading.Thread(target=self.ui.launch)

        self.game_thread.start()
        self.ui_thread.start()

        logging.info("Started !")
        self.game_thread.join()
        self.ui_thread.join()

        logging.info("Stopped")

    def stop(self):
        logging.info("Stopping...")
        set_app_alive(False)


def main():
    AppManager().start()


if __name__ == "__main__":
    main()
