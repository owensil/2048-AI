"""
file: board_view.py
copyright: Owen Siljander 2021
"""

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

    def _run_with_agent(self, ctr):
        assert ctr.event is not None
        while self._win.isOpen():
            self.update_graphics()
            update(15)
            ctr.event.set()

    def update_graphics(self):
        """
        Updates graphics
        Returns: Nothing
        """
        for item in self._win.items:
            item.undraw()
        self._draw_board()
        self._win.flush()

    def start(self, ctr):
        """
        Starts graphics display.
        Args:
            ctr: Calling controller object

        Returns: Nothing

        """
        assert ctr is not None
        self._win = GraphWin(title="2048 AI", width=self._win_size, height=self._win_size, autoflush=False)
        if not self._usr_input:
            self._run_with_agent(ctr)
            return
        listener = keyboard.Listener(on_press=ctr.consume_key, on_release=None)
        listener.start()
        while self._win.isOpen() and listener.running:
            self.update_graphics()
            update(15)
        if self._win.isOpen():
            self._win.close()
        if listener.running:
            listener.stop()
