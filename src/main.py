"""
file: main.py
copyright: Owen Siljander 2021
"""

import cProfile, pstats
from controller import Controller


def main():
    c = Controller()
    for i in range(1000):
        print("Iteration: ", i)
        c.run_random_agent()
        c.reset()


if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()
    main()
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('ncalls')
    stats.print_stats()
