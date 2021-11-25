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
            elif key == keyboard.Key.esc:
                # quit/kill thread
                exit(0)
        except AttributeError as e:
            # Ignore exceptions since they *should* only be caused by a user
            pass

    def run_agent(self, agent_type, graphics=False):
        agent = None
        if agent_type == 'DRAgent':
            agent = DRAgent(self._board)
        elif agent_type == 'Random':
            agent = RandomAgent(self._board)
        if graphics:
            self.event = Event()
            Thread(target=agent.play_graphics, args=[self.event]).start()
            BoardView(brd=self._board).start(self)
        else:
            agent.play()

    def run_interactive(self):
        # Runs the game with user controlled actions
        brd_view = BoardView(self._board, usr_input=True)
        brd_view.start(self)
