"""
file: controller.py
copyright: Owen Siljander 2021
"""

from board import Board
from board_view import BoardView
from random_agent import RandomAgent


class Controller:
    # ModelView
    def __init__(self):
        self.graphics = False
        self.board = Board()

    def reset(self):
        # Resets state to default
        self.graphics = False
        self.board = Board()

    def run_random_agent(self, graphics: bool = False):
        # Runs the random agent with graphics (optional)
        agent = RandomAgent(self.board)
        if graphics:
            brd_view = BoardView(brd=self.board)
            brd_view.start()
        agent.play()

    def run_interactive(self):
        # Runs the game with user controlled actions
        brd_view = BoardView(self.board, usr_input=True)
        brd_view.start()

