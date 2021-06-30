from graphics import *
from pynput import keyboard

from board import *


class Interactive:
    def __init__(self, brd: Board):
        self._key_listener = None
        self._win_size = None
        self._win = None
        self.brd = brd

    def _draw_board(self):
        """
        Draws the board on screen
        Returns: None

        """
        scale = (self._win_size - 20) / self.brd.get_board_size()
        top_left = Point(10, 10)
        bottom_right = Point(self._win_size - 10, self._win_size - 10)
        rect = Rectangle(top_left, bottom_right)
        assert (self.brd.get_board_size() > 1)
        for x in range(1, self.brd.get_board_size()):
            ratio = (self._win_size - 20) / self.brd.get_board_size()
            # Horizontal line
            hor = Line(Point(10 + ratio * x, 10), Point(10 + ratio * x, self._win_size - 10))
            # Vertical line
            vert = Line(Point(10, 10 + ratio * x), Point(self._win_size - 10, 10 + ratio * x))
            hor.draw(self._win)
            vert.draw(self._win)
        rect.draw(self._win)
        inside_offset = (self._win_size - 20) / (self.brd.get_board_size() * 2)
        # Draw background squares and tile numbers
        for i in range(0, self.brd.get_board_size() ** 2, self.brd.get_board_size()):
            for j in range(self.brd.get_board_size()):
                r = Rectangle(Point(10 + j * scale, 10 + (i // self.brd.get_board_size()) * scale),
                              Point(10 + j * scale + 2 * inside_offset,
                                    10 + (i // self.brd.get_board_size()) * scale + 2 * inside_offset))
                r.setFill(color_rgb(self._board[i + j] * 14, 100, 100))
                r.draw(self._win)
                if 2 ** self._board[i + j] == 1:
                    continue
                t = Text(Point(10 + j * scale + inside_offset, 10 + (i // self.brd.get_board_size()) * scale + inside_offset),
                         2 ** self._board[i + j])
                t.setSize(20)
                t.draw(self._win)

    def _on_press(self, key):
        """
        Event handler for keyboard. Used in interactive mode
        Args:
            key: Key that has been pressed

        Returns: Nothing

        """
        try:
            if key == keyboard.Key.right:
                # swipe right
                Board.swipe_right()
            elif key == keyboard.Key.left:
                # swipe left
                Board.swipe_left()
            elif key == keyboard.Key.up:
                # swipe up
                Board.swipe_up()
            elif key == keyboard.Key.down:
                # swipe down
                Board.swipe_down()
            else:
                self._key_listener.stop()
                self._win.close()
        except AttributeError:
            self._key_listener.stop()
            self._win.close()

    def start(self):
        self._key_listener = keyboard.Listener(on_press=self._on_press)
        self._win_size = 900
        self._win = GraphWin("2048 AI", self._win_size, self._win_size, autoflush=False)
        self._draw_board()
