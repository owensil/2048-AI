from abc import ABC, abstractmethod

from board import Board


class Agent(ABC):
    def __init__(self, board: Board):
        self._moves = 0
        self._board = board
        self._score = 0

    @abstractmethod
    def play(self):
        """
        Plays the game using the given board.
        Returns: None
        """
        pass

    def get_score(self):
        return self._score

    def get_board(self):
        return self._board
