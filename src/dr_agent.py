"""
file: dr_agent.py
copyright: Owen Siljander 2021
"""

from agent import Agent
from board import *
from threading import Event


class DRAgent(Agent):
    """
    Down-Right spamming agent.
    """
    def __init__(self, board: Board):
        super().__init__(board)
        random.seed(None)

    def _make_choice(self):
        moved = False
        direction = [self._board.swipe_down, self._board.swipe_right, self._board.swipe_left, self._board.swipe_up]
        # Priority move order of D-R-L-U
        # Make each choice until we have moved
        for i in range(4):
            moved = direction[i]()
            if moved:
                break

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
