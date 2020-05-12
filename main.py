def main():
	# Setup
	interactive = 1
	size = 4
	brd = Board(size)
	if interactive == 1:
		brd.start_interactive()


if __name__ == "__main__":
	main()