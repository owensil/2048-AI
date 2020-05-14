import random
from copy import deepcopy
from datetime import datetime
from math import inf

import numpy as np

# Learning rate
ALPHA = 0.001
# Size of the gameboard
SIZE = 4
# Value vectors used for q-learning
THETA = np.array([np.random.random((16,)), np.random.random((16,)), np.random.random((16,)), np.random.random((16,))])


def is_terminal(state) -> bool:
	"""
	Checks if game has ended. Pure function.
	Returns: bool indicating whether or not game has ended.
	"""
	end = True
	for i in range(SIZE ** 2):
		end = not ((state[i] == 0) or (
				(i + 1) % SIZE != 0 and state[i] == state[i + 1]) or (
				           i + SIZE < SIZE ** 2 and state[i] == state[i + SIZE]))
		if end is False:
			break
	return end


def spawn_piece(state):
	"""
	Spawns a piece in the state. A 2 with probability 0.9 and 4 with probability 0.1. Pure function.
	Returns: State with new piece spawned in it.
	"""
	arange = range(len(state))
	n_state = deepcopy(state)
	avail = [x for x in arange if state[x] == 0]
	if not avail:
		return state
	n_state[random.choice(avail)] = np.random.choice([1, 2], p=[0.9, 0.1])
	return n_state


def combiner(arange, state):
	"""
	Combines numbers along range, propagates out from start. This is a support method for actions. Non-pure function.
	Args:
		arange: Range to combine along
		state: list

	Returns: Reward from combining tiles

	"""
	prev = 0
	reward = 0
	moved = False
	for i in range(1, len(arange)):
		cur_val = state[arange[i]]
		if cur_val != 0:
			prev_val = state[arange[prev]]
			# Can combine in direction of swipe
			if prev_val == state[arange[i]]:
				state[arange[prev]] += 1
				reward += 2 ** prev_val
				state[arange[i]] = 0
				prev += 1
				moved = True
			# Can't combine (or zero)
			elif prev_val != cur_val:
				# Zero
				if prev_val != 0:
					prev += 1
					if prev == i:
						continue
				state[arange[prev]] = cur_val
				state[arange[i]] = 0
				moved = True
	# Penalize moves that don't do anything
	if not moved:
		reward -= 1
	return reward


def swipe_left(state):
	"""
	Moves pieces to the left. Non-pure function.
	Returns: reward
	"""
	reward = 0
	moved = False
	for i in range(0, SIZE ** 2, SIZE):
		arange = range(i, SIZE + i)
		r = combiner(arange, state)
		if r > 0:
			moved = True
			reward += r
	if not moved:
		return -1
	return reward


def swipe_right(state):
	"""
	Moves pieces to the right. Non-pure function.
	Returns: reward
	"""
	reward = 0
	moved = False
	for i in range(SIZE - 1, SIZE ** 2, SIZE):
		arange = range(i, i - SIZE, -1)
		r = combiner(arange, state)
		if r > 0:
			moved = True
			reward += r
	if not moved:
		return -1
	return reward


def swipe_up(state):
	"""
	Moves pieces up. Non-pure function.
	Returns: reward
	"""
	reward = 0
	moved = False
	for i in range(0, SIZE, 1):
		arange = range(i, SIZE ** 2, SIZE)
		r = combiner(arange, state)
		if r > 0:
			moved = True
			reward += r
	if not moved:
		return -1
	return reward


def swipe_down(state):
	"""
	Moves pieces down. Non-pure function.
	Returns: reward
	"""
	reward = 0
	moved = False
	for i in range((SIZE - 1) * SIZE, SIZE ** 2, 1):
		arange = range(i, -1, -SIZE)
		r = combiner(arange, state)
		if r > 0:
			moved = True
			reward += r
	if not moved:
		return -1
	return reward


def evaluate(state, action):
	"""
	Returns the estimated value of a state
	Args:
		state:
		action:

	Returns:

	"""
	garb, reward = compute_afterstate(state, action)
	if reward < 0:
		return -1
	return np.matmul(THETA[action], state)


def compute_afterstate(state, action):
	"""
	Computes the afterstate (before random piece spawn). Pure function.
	Args:
		state: Game state
		action: Action to execute (integer)

	Returns: State after executing action and reward gained by action
	"""
	s_prime = deepcopy(state)
	if action == 0:
		reward = swipe_left(s_prime)
	elif action == 1:
		reward = swipe_right(s_prime)
	elif action == 2:
		reward = swipe_up(s_prime)
	elif action == 3:
		reward = swipe_down(s_prime)
	else:
		raise ValueError("Incorrect move")
	return s_prime, reward


def make_move(state, action):
	"""
	Makes a move.
	Args:
		state: State of the game
		action: Action [0-3]

	Returns: Reward, state after action, state after action and generating tile

	"""
	s_prime, reward = compute_afterstate(state, action)
	s_dprime = spawn_piece(s_prime)
	return reward, s_prime, s_dprime


def learn_evaluation(state, action, reward, s_prime, s_dprime):
	v_next = np.max([np.matmul(THETA[i], s_dprime) for i in range(3)])
	temp = np.matmul(THETA[action], state)
	THETA[action] = temp + ALPHA * (reward + v_next - temp)
	THETA[action] = np.interp(THETA[action], (np.min(THETA[action]), np.max(THETA[action])), (0, 65536))


def play_game():
	learning_enabled = True
	score = 0
	# Init
	state = np.zeros(16)
	spawn_piece(state)
	# While not terminal
	while not is_terminal(state):
		# argmax
		max_val = -inf
		action = -1
		for i in range(3):
			ret = evaluate(state, i)
			if ret > max_val:
				max_val = ret
				action = i
		# Make move
		assert action != -1
		reward, s_prime, s_dprime = make_move(state, action)
		if learning_enabled:
			learn_evaluation(state, action, reward, s_prime, s_dprime)
		score += reward
		state = s_dprime
	return score


def main():
	score = None
	try:
		weight_file = open("weight_file.txt", 'a+')
		dt = datetime.now()
		weight_file.write("Cur time: " + str(dt.microsecond) + "\n")
	except IOError as e:
		print("Failed to open file for weights")
		return
	for x in range(1000):
		try:
			score = play_game()
			print("Game: ", x, " Score: ", score)
		except BaseException as e:
			print(e)
			break
	if not weight_file.closed:
		weight_file.write(str(THETA) + '\n')
		weight_file.close()


if __name__ == "__main__":
	main()
