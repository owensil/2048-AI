from sys import stderr
from threading import Thread

from graphics import *
from pynput import keyboard

from board import *


class BoardView:
    def __init__(self, win_size: int = 900, brd: Board = None):
        """
        Constructor for game visualizer
        Args:
            win_size: Size of the graphics window (default 900)
            brd: Game board to display (default None)
        """
        self._brd = brd
        self._win_size = win_size
        self._key_listener = None
        self._win = None

    def _draw_board(self):
        """
        Draws the board on screen
        Returns: None

        """
        try:
            assert (self._brd.get_board_size() > 1)
        except AssertionError as e:
            print("Board has non-positive size", file=stderr)
            raise e
        scale = (self._win_size - 20) / self._brd.get_board_size()
        top_left = Point(10, 10)
        bottom_right = Point(self._win_size - 10, self._win_size - 10)
        rect = Rectangle(top_left, bottom_right)
        for x in range(1, self._brd.get_board_size()):
            ratio = (self._win_size - 20) / self._brd.get_board_size()
            # Horizontal line
            hor = Line(Point(10 + ratio * x, 10), Point(10 + ratio * x, self._win_size - 10))
            # Vertical line
            vert = Line(Point(10, 10 + ratio * x), Point(self._win_size - 10, 10 + ratio * x))
            hor.draw(self._win)
            vert.draw(self._win)
        rect.draw(self._win)
        inside_offset = (self._win_size - 20) / (self._brd.get_board_size() * 2)
        # Draw background squares and tile numbers
        for i in range(0, self._brd.get_board_size() ** 2, self._brd.get_board_size()):
            for j in range(self._brd.get_board_size()):
                r = Rectangle(Point(10 + j * scale, 10 + (i // self._brd.get_board_size()) * scale),
                              Point(10 + j * scale + 2 * inside_offset,
                                    10 + (i // self._brd.get_board_size()) * scale + 2 * inside_offset))
                r.setFill(color_rgb(235, (220 - self._brd.get_datum(i + j) * 14) % 255, 52))
                r.draw(self._win)
                if 2 ** self._brd.get_datum(i + j) == 1:
                    continue
                t = Text(Point(10 + j * scale + inside_offset,
                               10 + (i // self._brd.get_board_size()) * scale + inside_offset),
                         2 ** self._brd.get_datum(i + j))
                t.setSize(20)
                t.draw(self._win)

    def update_graphics(self):
        """
        Used for forcing graphic updates
        Returns: None
        """
        for item in self._win.items[:]:
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
                self._brd.swipe_right()
            elif key == keyboard.Key.left:
                # swipe left
                self._brd.swipe_left()
            elif key == keyboard.Key.up:
                # swipe up
                self._brd.swipe_up()
            elif key == keyboard.Key.down:
                # swipe down
                self._brd.swipe_down()
            else:
                self._key_listener.stop()
                self._win.close()
        except AttributeError as e:
            self._key_listener.stop()
            self._win.close()
            raise e

    def _on_release(self, key):
        pass

    def start(self):
        self._win = GraphWin("2048 AI", self._win_size, self._win_size, autoflush=False)
        self._key_listener = keyboard.Listener(on_press=self._on_press, on_release=self._on_release)
        self._draw_board()
        self._key_listener.start()
        # Feels hacky to me but tkinter refuses to not be in the main thread
        while self._key_listener.running:
            self.update_graphics()
            update(15)

    def set_board(self, brd: Board):
        self._brd = brd
