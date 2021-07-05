import random

import numpy as np


class Board:
    def __init__(self, size=4):
        """
        Initializer for 2048 game board
        Args:
            size: Integer size of the board, must be greater than 0. Size represents the square size
                (e.g. 8 would be a chessboard). Default size is 4.
        """
        if size <= 0:
            raise ValueError("Board size must be positive")
        random.seed(None)
        self._board = np.zeros(size ** 2, int)
        self._size = size
        self._game_ended = False
        self._score = 0
        self._spawn_piece()

    def _spawn_piece(self):
        """
        Spawns a piece on the board. A 2 with probability 0.9 and 4 with probability 0.1
        """
        avail = [x for x in range(len(self._board)) if self._board[x] == 0]
        self._board[random.choice(avail)] = np.random.choice([1, 2], p=[0.9, 0.1])

    def _combiner(self, block):
        """
        Combines numbers along range, propagates out from start. This is a support method for actions. Action functions
        input a "custom range" (e.g. 0,4,8,12 would be a vertical range) and this function combines along it.
        Args:
            block: Range to combine along

        Returns: Whether or not any tiles changed position (boolean)

        """
        moved = False
        prev = 0
        # TODO: Add scoring
        for i in range(1, len(block)):
            if self._board[block[i]] != 0:
                # Can combine in direction of swipe
                if self._board[block[prev]] == self._board[block[i]]:
                    self._board[block[prev]] += 1
                    self._board[block[i]] = 0
                    prev += 1
                    moved = True
                # Can't combine (or zero)
                elif self._board[block[prev]] != self._board[block[i]]:
                    # Zero
                    if self._board[block[prev]] != 0:
                        prev += 1
                        if prev == i:
                            continue
                    self._board[block[prev]] = self._board[block[i]]
                    self._board[block[i]] = 0
                    moved = True
        return moved

    def swipe_left(self) -> bool:
        """
        Moves pieces to the left
        Returns: 0 on success, 1 otherwise
        """
        moved = False
        for i in range(0, self._size ** 2, self._size):
            block = range(i, self._size + i)
            moved = self._combiner(block) or moved
        if moved:
            self._spawn_piece()
        return moved

    def swipe_right(self) -> bool:
        """
        Moves pieces to the right
        Returns: 0 on success, 1 otherwise
        """
        moved = False
        for i in range(self._size - 1, self._size ** 2, self._size):
            block = range(i, i - self._size, -1)
            moved = self._combiner(block) or moved
        if moved:
            self._spawn_piece()
        return moved

    def swipe_up(self) -> bool:
        """
        Moves pieces up
        Returns: 0 on success, 1 otherwise

        """
        moved = False
        for i in range(0, self._size, 1):
            block = range(i, self._size ** 2, self._size)
            moved = self._combiner(block) or moved
        if moved:
            self._spawn_piece()
        return moved

    def swipe_down(self) -> bool:
        """
        Moves pieces down
        Returns: 0 on success, 1 otherwise

        """
        moved = False
        for i in range((self._size - 1) * self._size, self._size ** 2, 1):
            block = range(i, -1, -self._size)
            moved = self._combiner(block) or moved
        if moved:
            self._spawn_piece()
        return moved

    def is_terminal(self) -> bool:
        """
        Checks if game has ended
        Returns: bool
        """
        end = True
        for i in range(self._size ** 2):
            # Zero tile or tile can combine right or tile can combine below
            # Since this starts from top left, no need to check left or above neighbors
            end = not ((self._board[i] == 0) or (
                    (i + 1) % self._size != 0 and self._board[i] == self._board[i + 1]) or (
                               i + self._size < self._size ** 2 and self._board[i] == self._board[i + self._size]))
            if end is False:
                break
        return end

    def reset(self):
        self._board = np.zeros((self._size, self._size))
        self._score = 0
        self._spawn_piece()

    def get_board_data(self):
        """
        Gets the entire board data
        Returns: 1D list of board data
        """
        return self._board

    def get_datum(self, pos: int):
        """
        Gets single datum from the game board
        Args:
            pos: Position of datum (note: board data is 1D)
        Returns: Datum at the position specified
        """
        return self._board[pos]

    def get_board_size(self):
        """
        Returns: The single side size of the game board.
        """
        return self._size
