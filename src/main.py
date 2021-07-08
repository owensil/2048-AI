# from tensorforce import Agent
# from tensorforce.execution import Runner
import threading

from board import Board
from board_view import BoardView
from random_agent import RandomAgent


def run_random_agent(graphics: bool):
    """

    Args:
        graphics: True to enable graphics
    """
    board = Board()
    agent = RandomAgent(board)
    th = threading.Thread(target=RandomAgent.play, args=(agent,))
    if graphics:
        brd_view = BoardView(brd=board)
        brd_view.start()
    th.start()


def run_interactive():
    board = Board()
    brd_view = BoardView(brd=board, usr_input=True)
    brd_view.start()


def main():
    # run_random_agent(True)
    run_interactive()

if __name__ == "__main__":
    main()
