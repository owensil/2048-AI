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
        b._check_end()
        self.assertEqual(True, b.game_ended)
        # Zero check
        b._board = [
            2, 4, 2, 4,
            4, 2, 4, 2,
            2, 4, 2, 4,
            4, 2, 0, 2
        ]
        b._check_end()
        self.assertEqual(False, b.game_ended)
        # Right or left
        b._board = [
            2, 4, 2, 4,
            4, 2, 4, 2,
            2, 4, 8, 4,
            4, 2, 2, 2
        ]
        b._check_end()
        self.assertEqual(False, b.game_ended)
        # Up or down
        b._board = [
            2, 4, 2, 4,
            4, 2, 4, 2,
            2, 4, 8, 4,
            4, 2, 8, 2
        ]
        b._check_end()
        self.assertEqual(False, b.game_ended)


if __name__ == '__main__':
    unittest.main()
