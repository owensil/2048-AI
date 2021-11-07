"""
file: board_view.py
copyright: Owen Siljander 2021
"""

from sys import stderr

from graphics import *
from pynput import keyboard

from board import *
from queue import Queue


class BoardView:
    def __init__(self, brd: Board = None, usr_input: bool = False, win_size: int = 900):
        """
        Constructor for game visualizer
        Args:
            brd: Game board to display (default None)
            usr_input: Determines if the viewer will listen for user input or not
            win_size: Size of the graphics window (default 900)
        """
        self._board = brd
        self._win_size = win_size
        self._key_listener = None
        self._win = None
        self._usr_input = usr_input

    def _draw_board(self):
        """
        Draws the board on screen
        Returns: None

        """
        brd_size = self._board.get_board_size()
        # Outline, offset by 10 pixels, could extract offset into a variable but no real point at the moment
        rect = Rectangle(Point(10, 10), Point(self._win_size - 10, self._win_size - 10))
        rect.draw(self._win)
        # Draw grid
        ratio = (self._win_size - 20) / self._board.get_board_size()
        for x in range(1, brd_size):
            # Horizontal line
            hor = Line(Point(10 + ratio * x, 10), Point(10 + ratio * x, self._win_size - 10))
            hor.draw(self._win)
            # Vertical line
            vert = Line(Point(10, 10 + ratio * x), Point(self._win_size - 10, 10 + ratio * x))
            vert.draw(self._win)
        # Draw background squares and tile numbers
        inside_offset = (self._win_size - 20) / (brd_size * 2)
        scale = (self._win_size - 20) / brd_size
        for i in range(0, brd_size ** 2, brd_size):
            for j in range(brd_size):
                r = Rectangle(Point(10 + j * scale, 10 + (i // brd_size) * scale),
                              Point(10 + j * scale + 2 * inside_offset,
                                    10 + (i // brd_size) * scale + 2 * inside_offset))
                r.setFill(color_rgb(235, (220 - self._board.get_datum(i + j) * 14) % 255, 52))
                r.draw(self._win)
                # Don't draw tile numbers if they're zero
                if 2 ** self._board.get_datum(i + j) == 1:
                    continue
                t = Text(Point(10 + j * scale + inside_offset,
                               10 + (i // brd_size) * scale + inside_offset),
                         2 ** self._board.get_datum(i + j))
                t.setSize(20)
                t.draw(self._win)
        score = Text(Point(30, 30), self._board.get_score())
        score.draw(self._win)

    def update_graphics(self):
        """
        Used for forcing graphic updates
        Returns: None
        """
        for item in self._win.items:
            item.undraw()
        self._draw_board()
        self._win.flush()

    def _on_press(self, key):
        """
        Event handler for keyboard. Used in interactive mode
        Args:
            key: Key that has been pressed

        Returns: Nothing

        """
        print("On press called")
        try:
            if key == keyboard.Key.right:
                # swipe right
                self._board.swipe_right()
            elif key == keyboard.Key.left:
                # swipe left
                self._board.swipe_left()
            elif key == keyboard.Key.up:
                # swipe up
                self._board.swipe_up()
            elif key == keyboard.Key.down:
                # swipe down
                self._board.swipe_down()
            else:
                return False
            self.update_graphics()
        except AttributeError as e:
            self._key_listener.stop()
            self._win.close()
            raise e

    def _on_release(self, key):
        pass

    def start(self):
        """
        Display graphics.
        Returns: None

        """
        self._win = GraphWin("2048 AI", self._win_size, self._win_size, autoflush=False)
        self._win.create_window()
        if self._usr_input:
            listener = keyboard.Listener(on_press=self._on_press, on_release=self._on_release)
            listener.start()

        else:
            while True:
                self.update_graphics()
                update(60)
