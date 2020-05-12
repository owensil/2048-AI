# Random agent

import random

from board import Board


class RandomAgent:
	def __init__(self):
		random.seed(None)

	@staticmethod
	def make_choice(game_board: Board):
		"""
		Makes a random choice on the 2048 game board
		Args:
			game_board: 2048 gameboard

		Returns:

		"""
		choice = random.choice(range(4))
		if choice == 0:
			game_board.swipe_left()
		elif choice == 1:
			game_board.swipe_right()
		elif choice == 2:
			game_board.swipe_up()
		elif choice == 3:
			game_board.swipe_down()
