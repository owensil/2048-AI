"""
file: main.py
copyright: Owen Siljander 2021
"""

import cProfile, pstats
from controller import Controller


def main():
    c = Controller()
    c.run_interactive()


if __name__ == "__main__":
    main()
