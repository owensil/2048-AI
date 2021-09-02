from abc import ABC, abstractmethod

from board import Board


class Agent(ABC):
    def __init__(self, board: Board):
        self._moves = 0
        self._board = board

    @abstractmethod
    def play(self):
        """
        Plays the game using the given board.
        Returns: None
        """
        pass

    def get_score(self):
        return self._board.get_score()

    def get_board(self):
        return self._board
