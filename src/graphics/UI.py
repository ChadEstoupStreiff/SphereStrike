import logging
import threading
import tkinter as tk
from time import sleep

from core import current_time, get_env_values, is_app_alive, from_rgb
from game import GameManager


class GameUI:
    def __init__(self, linked_game: GameManager) -> None:
        self.linked_game = linked_game
        self.tick = 0

        self.average_last_tick = 0
        self.average_fps = 0

        self.tk_thread = None
        self.avg_thread = None

        self.root = None
        self.game_root = None
        self.game_canva = None
        self.show_game = None

    def launch(self):
        self.tk_thread = threading.Thread(target=self.tk_ui)
        self.tk_thread.start()

        self.avg_thread = threading.Thread(target=self.second_tick)
        self.avg_thread.start()

        self.tk_thread.join()
        self.avg_thread.join()

    def tk_ui(self):
        logging.debug("Starting game_tick ui thread")
        self.create_ui()
        while is_app_alive():
            start = current_time()

            # ROOT tick
            l = tk.Label(self.root, text=f"FPS: {self.average_fps}")
            l.grid(column=1, row=1)

            l = tk.Label(self.root, text=f"TPS: {self.linked_game.average_tps}")
            l.grid(column=2, row=1)

            self.root.update()

            # GAME canva tick
            if self.game_canva is not None:
                self.game_canva.delete("all")

                for player in self.linked_game.players:
                    self.game_canva.create_oval(
                        player.X - player.size,
                        int(get_env_values("TERRAIN_Y_SIZE")) - player.Y - player.size,
                        player.X + player.size,
                        int(get_env_values("TERRAIN_Y_SIZE")) - player.Y + player.size,
                        fill="yellow",
                        width=0,
                    )

                for ball in self.linked_game.balls:
                    speed_rgb = min(int(ball.get_speed()/2), 255)
                    self.game_canva.create_oval(
                        ball.X - ball.size,
                        int(get_env_values("TERRAIN_Y_SIZE")) - ball.Y - ball.size,
                        ball.X + ball.size,
                        int(get_env_values("TERRAIN_Y_SIZE")) - ball.Y + ball.size,
                        fill=from_rgb(speed_rgb, 100, 255 - speed_rgb),
                        width=0,
                    )

                self.game_canva.update()

            self.tick += 1
            end = current_time()
            sleep(max(0, (1000.0 / int(get_env_values("FPS")) - end + start) / 1000.0))
        self.root.destroy()
        if self.game_root is not None:
            self.game_root.destroy()
        logging.debug("End game_tick ui thread")

    def second_tick(self):
        logging.debug("Starting second_tick game thread")
        while is_app_alive():
            sleep(1)

            self.average_fps = self.tick - self.average_last_tick
            self.average_last_tick = self.tick

            if self.average_fps < int(get_env_values("FPS")) - 1:
                logging.warning(f"Average FPS: {self.average_fps}")
            else:
                logging.debug(f"Average FPS: {self.average_fps}")
        logging.debug("Ending game_tick game thread")

    def create_ui(self):
        self.root = tk.Tk()
        self.root.geometry("500x500")

        self.show_game = tk.BooleanVar(value=True)
        self.show_game_button_callback()

        c1 = tk.Checkbutton(
            self.root,
            text="Show game",
            variable=self.show_game,
            onvalue=True,
            offvalue=False,
            command=self.show_game_button_callback,
        )
        c1.grid(column=0, row=1)

    def show_game_button_callback(self):
        if self.show_game.get() and self.game_root is None:
            self.game_root = tk.Tk()
            self.game_root.bind('<KeyPress>', self.onKeyPress)
            self.game_canva = tk.Canvas(
                self.game_root,
                bg="black",
                width=get_env_values("TERRAIN_X_SIZE"),
                height=get_env_values("TERRAIN_Y_SIZE"),
            )
            self.game_canva.pack()
        elif not self.show_game.get() and self.game_root is not None:
            self.game_canva = None
            self.game_root.destroy()
            self.game_root = None

    def onKeyPress(self, event):
        logging.debug(f"You pressed {event.char}")