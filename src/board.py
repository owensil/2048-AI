import random
from copy import deepcopy
from math import inf

import numpy as np


class Board:
    def __init__(self, size=4):
        """
        Initialzier for 2048 game board
        Args:
            size: Integer size of the board, must be greater than 0. Size represents the square size
                (e.g. 8 would be a chessboard). Default size is 4.
        """
        if size == 0:
            raise ValueError("Board size can't be zero")
            return
        random.seed(None)
        self._board = np.zeros(size ** 2, int)
        self._board_size = size
        self._game_ended = False
        self._score = 0
        self._learning_rate = 0.001
        self._epsilon = 0.1
        self._spawn_piece()

    def _spawn_piece(self):
        """
        Spawns a piece on the board. A 2 with probability 0.9 and 4 with probability 0.1
        """
        direction = range(len(self._board))
        avail = [x for x in direction if self._board[x] == 0]
        self._board[random.choice(avail)] = np.random.choice([1, 2], p=[0.9, 0.1])

    # TODO below

    def _combiner(self, arange):
        """
        Combines numbers along range, propagates out from start. This is a support method for actions
        Args:
            arange: Range to combine along

        Returns: Whether or not any tiles changed position (boolean)

        """
        moved = False
        prev = 0
        for i in range(1, len(arange)):
            if self._board[arange[i]] != 0:
                # Can combine in direction of swipe
                if self._board[arange[prev]] == self._board[arange[i]]:
                    self._board[arange[prev]] += 1
                    self._board[arange[i]] = 0
                    prev += 1
                    moved = True
                # Can't combine (or zero)
                elif self._board[arange[prev]] != self._board[arange[i]]:
                    # Zero
                    if self._board[arange[prev]] != 0:
                        prev += 1
                        if prev == i:
                            continue
                    self._board[arange[prev]] = self._board[arange[i]]
                    self._board[arange[i]] = 0
                    moved = True
        return moved

    def _swipe_left(self, ) -> bool:
        """
        Moves pieces to the left
        Returns: 0 on success, 1 otherwise
        """
        moved = False
        for i in range(0, SIZE ** 2, SIZE):
            arange = range(i, SIZE + i)
            moved = self._combiner(arange) or moved
        return moved

    def _swipe_right(self) -> bool:
        """
        Moves pieces to the right
        Returns: 0 on success, 1 otherwise
        """
        moved = False
        for i in range(SIZE - 1, SIZE ** 2, SIZE):
            arange = range(i, i - SIZE, -1)
            moved = self._combiner(arange) or moved
        return moved

    def _swipe_up(self) -> bool:
        """
        Moves pieces up
        Returns: 0 on success, 1 otherwise

        """
        moved = False
        for i in range(0, SIZE, 1):
            arange = range(i, SIZE ** 2, SIZE)
            moved = self._combiner(arange) or moved
        return moved

    def _swipe_down(self) -> bool:
        """
        Moves pieces down
        Returns: 0 on success, 1 otherwise

        """
        moved = False
        for i in range((SIZE - 1) * SIZE, SIZE ** 2, 1):
            arange = range(i, -1, -SIZE)
            moved = self._combiner(arange) or moved
        return moved

    def is_terminal(self) -> bool:
        """
        Checks if game has ended
        Returns: bool
        """
        end = True
        for i in range(SIZE ** 2):
            end = not ((self._board[i] == 0) or (
                    (i + 1) % SIZE != 0 and self._board[i] == self._board[i + 1]) or (
                               i + SIZE < SIZE ** 2 and self._board[i] == self._board[i + SIZE]))
            if end is False:
                break
        return end

    def reset(self):
        self._board = np.zeros((SIZE, SIZE))
        self.score = 0
        self._spawn_piece()

    def get_board_data(self):
        return self._board

    def get_datum(self, pos: int):
        return self._board[pos]

    def get_board_size(self):
        return len(self._board) ** (1 / 2)

    def evaluate(self, state, action):
        return np.matmul(self._val_funcs[action], state)

    # TODO: This needs refactoring to not be static
    @staticmethod
    def compute_afterstate(state, action):
        s_prime = deepcopy(state)
        if action == 0:
            Board._swipe_left(s_prime)
        elif action == 1:
            Board._swipe_right(s_prime)
        elif action == 2:
            Board._swipe_up(s_prime)
        elif action == 3:
            Board._swipe_down(s_prime)
        else:
            raise ValueError("Incorrect move")

    # TODO: This needs refactoring to not be static
    @staticmethod
    def make_move(state, action):
        s_prime, reward = Board.compute_afterstate(state, action)
        s_dprime = Board._spawn_piece(s_prime)
        return reward, s_prime, s_dprime

    # TODO: Should not be part of the board class
    def learn_evaluation(self, state, action, reward, s_prime, s_dprime):
        v_next = None
        max = -inf
        for i in [0, 1, 2, 3]:
            pass

    # TODO: Should not be part of the board class
    def play_game(self):
        learning_enabled = True
        score = 0
        # Init
        state = np.zeros(16)
        Board._spawn_piece(state)
        # While not terminal
        while not Board.is_terminal(state):
            # argmax
            max_val = -inf
            action = -1
            for i in [0, 1, 2, 3]:
                ret = self.evaluate(state, i)
                if ret > max_val:
                    max_val = ret
                    action = i
            # Make move
            assert action != -1
            reward, s_prime, s_dprime = Board.make_move(state, action)
            if learning_enabled:
                Board.learn_evaluation(state, action, reward, s_prime, s_dprime)
            score += reward
            state = s_dprime
        return score
