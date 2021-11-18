"""
file: random_agent.py
copyright: Owen Siljander 2021
"""

from agent import Agent
from board import *
from threading import Event


class RandomAgent(Agent):
    """
    Agent that makes uniformly random moves.
    """
    def __init__(self, board: Board):
        super().__init__(board)
        random.seed(None)

    def _make_choice(self):
        choice = random.choice(range(4))
        if choice == 0:
            self._board.swipe_left()
        elif choice == 1:
            self._board.swipe_right()
        elif choice == 2:
            self._board.swipe_up()
        elif choice == 3:
            self._board.swipe_down()

    def play(self):
        while not self._board.is_terminal():
            self._make_choice()

    def play_graphics(self, event: Event):
        """
        Purposely delayed random agent. Just for fun so you can actually
        watch the agent play using graphics (instead of it just finishing immediately)
        Returns: Nothing

        """
        while not self._board.is_terminal():
            event.wait()
            self._make_choice()
            event.clear()
