import unittest

from src.board import Board


class BoardTest(unittest.TestCase):

    def test_game_end(self):
        # Can't move
        b = Board()
        b._board = [
            2, 4, 2, 4,
            4, 2, 4, 2,
            2, 4, 2, 4,
            4, 2, 4, 2
        ]
        self.assertEqual(True, b.is_terminal())
        # Zero check
        b._board = [
            2, 4, 2, 4,
            4, 2, 4, 2,
            2, 4, 2, 4,
            4, 2, 0, 2
        ]
        self.assertEqual(False, b.is_terminal())
        # Right or left
        b._board = [
            2, 4, 2, 4,
            4, 2, 4, 2,
            2, 4, 8, 4,
            4, 2, 2, 2
        ]
        self.assertEqual(False, b.is_terminal())
        # Up or down
        b._board = [
            2, 4, 2, 4,
            4, 2, 4, 2,
            2, 4, 8, 4,
            4, 2, 8, 2
        ]
        self.assertEqual(False, b.is_terminal())

    def test_combine(self):
        # Individual checks of squares are needed because of the stochastic elements
        b = Board()

        # Right swipe
        b._board = [
            2, 0, 0, 2,
            2, 2, 0, 0,
            0, 0, 2, 2,
            0, 2, 0, 2
        ]
        b.swipe_right()
        self.assertEqual(3, b._board[3])
        self.assertEqual(3, b._board[7])
        self.assertEqual(3, b._board[11])
        self.assertEqual(3, b._board[15])

        # Left swipe
        b._board = [
            2, 0, 0, 2,
            2, 2, 0, 0,
            0, 0, 2, 2,
            0, 2, 0, 2
        ]
        b.swipe_left()
        self.assertEqual(3, b._board[0])
        self.assertEqual(3, b._board[4])
        self.assertEqual(3, b._board[8])
        self.assertEqual(3, b._board[12])

        # Up swipe
        b._board = [
            2, 0, 0, 2,
            2, 2, 0, 0,
            0, 0, 2, 2,
            0, 2, 0, 2
        ]
        b.swipe_up()
        self.assertEqual(3, b._board[0])
        self.assertEqual(3, b._board[1])
        self.assertEqual(2, b._board[2])
        self.assertEqual(3, b._board[3])
        self.assertEqual(2, b._board[7])

        # Down swipe
        b._board = [
            2, 0, 0, 2,
            2, 2, 0, 0,
            0, 0, 2, 2,
            0, 2, 0, 2
        ]
        b.swipe_down()
        self.assertEqual(3, b._board[12])
        self.assertEqual(3, b._board[13])
        self.assertEqual(2, b._board[14])
        self.assertEqual(3, b._board[15])
        self.assertEqual(2, b._board[11])


if __name__ == '__main__':
    unittest.main()
