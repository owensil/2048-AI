from board import *
from random_agent import RandomAgent


def main():
	# Setup
	interactive = 0
	size = 4
	brd = Board(size, graphics=0)
	rand_ag = RandomAgent()
	if interactive == 1:
		brd.start_interactive()
	while not brd.game_ended:
		rand_ag.make_choice(brd)


# brd.update_graphics()


if __name__ == "__main__":
	main()
