"""
file: controller.py
copyright: Owen Siljander 2021
"""

from board import Board
from board_view import BoardView
from random_agent import RandomAgent
from dr_agent import DRAgent
from pynput import keyboard
from threading import Thread, Event


class Controller:
    # ModelView
    def __init__(self):
        self._board = Board()
        self.event = None

    def consume_key(self, key: keyboard.Key):
        # Callback for user input
        try:
            if key == keyboard.Key.right:
                # swipe right
                self._board.swipe_right()
            elif key == keyboard.Key.left:
                # swipe left
                self._board.swipe_left()
            elif key == keyboard.Key.up:
                # swipe up
                self._board.swipe_up()
            elif key == keyboard.Key.down:
                # swipe down
                self._board.swipe_down()
        except AttributeError as e:
            # Ignore exceptions since they *should* only be caused by a user
            pass

    def run_dl_agent_graphics(self):
        agent = DRAgent(self._board)
        self.event = Event()
        Thread(target=agent.play_graphics, args=[self.event]).start()
        brd_view = BoardView(brd=self._board)
        brd_view.start(self)

    def run_dl_agent(self):
        agent = DRAgent(self._board)
        agent.play()

    def run_random_agent_graphics(self):
        # Runs the random agent with graphics
        agent = RandomAgent(self._board)
        self.event = Event()
        Thread(target=agent.play_graphics, args=[self.event]).start()
        brd_view = BoardView(brd=self._board)
        brd_view.start(self)

    def run_random_agent(self):
        # Runs the random agent
        agent = RandomAgent(self._board)
        agent.play()

    def run_interactive(self):
        # Runs the game with user controlled actions
        brd_view = BoardView(self._board, usr_input=True)
        brd_view.start(self)
