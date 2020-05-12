import random

import numpy as np
from graphics import *
from pynput import keyboard

class Board:
	def __init__(self, size, graphics=1):
		random.seed(None)
		self._win_size = 900
		self._board = np.zeros((size, size))
		self._size = size
		self._win = None
		if graphics == 1:
			self._win = GraphWin("2048 AI", self._win_size, self._win_size)
			self._draw_board()

	def _draw_board(self):
		top_left = Point(10, 10)
		bottom_right = Point(self._win_size - 10, self._win_size - 10)
		rect = Rectangle(top_left, bottom_right)
		assert (self._size > 1)
		for x in range(1, self._size):
			ratio = (self._win_size - 20) / self._size
			# Horizontal line
			hor = Line(Point(10 + ratio * x, 10), Point(10 + ratio * x, self._win_size - 10))
			# Vertical line
			vert = Line(Point(10, 10 + ratio * x), Point(self._win_size - 10, 10 + ratio * x))
			hor.draw(self._win)
			vert.draw(self._win)
		rect.draw(self._win)

	def _spawn_piece(self):
		"""
		Spawns a piece on the _board. A 2 with probability 0.9 and 4 with probability 0.1
		"""
		# Make random choice between 2 and 4
		val = np.random.choice([2, 4], p=[0.9, 0.1])
		# Pick random available square
		avail = []
		for x in range(0, self._size):
			for y in range(0, self._size):
				if self._board[x][y] == 0:
					avail.append([x, y])
		loc = random.choice(avail)
		self._board[loc] = val
		print("Chose: ", val)
		print("Location: ", loc)

	def _on_press(self, key):
		"""
		Event handler for keyboard. Used in interactive mode
		Args:
			key: Key that has been pressed

		Returns: Nothing

		"""
		try:
			print('alphanumeric key {0} pressed'.format(
				key.char))
		except AttributeError:
			if key == keyboard.Key.right:
				# swipe right
				self.swipe_right()
			elif key == keyboard.Key.left:
				# swipe left
				self.swipe_left()
			elif key == keyboard.Key.up:
				# swipe up
				self.swipe_up()
			elif key == keyboard.Key.down:
				# swipe down
				self.swipe_down()

	def _on_release(self, key):
		"""
		Event handler for keyboard. Used in interactive mode
		Args:
			key: Key that has been pressed

		Returns: Nothing

		"""
		pass

	def swipe_left(self) -> int:
		"""
		Moves pieces to the left
		Returns: 0 on success, 1 otherwise

		"""
		pass

	def swipe_right(self) -> int:
		"""
		Moves pieces to the right
		Returns: 0 on success, 1 otherwise

		"""
		pass

	def swipe_up(self) -> int:
		"""
		Moves pieces up
		Returns: 0 on success, 1 otherwise

		"""
		pass

	def swipe_down(self) -> int:
		"""
		Moves pieces down
		Returns: 0 on success, 1 otherwise

		"""
		pass

	def start_interactive(self):
		"""
		Starts 2048 in interactive mode
		Returns: Nothing
		"""
		# Event listeners
		listener = keyboard.Listener(
			on_press=self._on_press,
			on_release=self._on_release)
		listener.start()
