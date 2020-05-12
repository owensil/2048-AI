from board import *


def main():
	# Setup
	interactive = 1
	size = 4
	brd = Board(size)
	if interactive == 1:
		brd.start_interactive()


# print("lef")
# brd.swipe_left()
# print('ri')
# brd.swipe_right()
# print('up')
# brd.swipe_up()
# print('down')
# brd.swipe_down()


if __name__ == "__main__":
	main()
