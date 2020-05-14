import random
from copy import deepcopy, copy
from datetime import datetime
from math import inf
import tensorflow as tf
from tensorflow import keras

import numpy as np

# Learning rate
ALPHA = 0.001
# Size of the gameboard
SIZE = 4
# Value vectors used for q-learning
try:
	THETA = [keras.models.load_model("tf_model0.h5"), keras.models.load_model("tf_model1.h5"),
	         keras.models.load_model("tf_model2.h5"), keras.models.load_model("tf_model3.h5")]
except BaseException as e:
	print("\n\n!======== UNABLE TO LOAD MODELS - CREATING MODELS... ==========!\n\n")
	model1 = keras.Sequential([
		keras.layers.Dense(4, activation='relu', input_shape=(16,)),
		keras.layers.Dense(1)
	])
	model2 = keras.Sequential([
		keras.layers.Dense(4, activation='relu', input_shape=(16,)),
		keras.layers.Dense(1)
	])
	model3 = keras.Sequential([
		keras.layers.Dense(4, activation='relu', input_shape=(16,)),
		keras.layers.Dense(1)
	])
	model4 = keras.Sequential([
		keras.layers.Dense(4, activation='relu', input_shape=(16,)),
		keras.layers.Dense(1)
	])

	THETA = np.array([model1, model2, model3, model4])

	for model in THETA:
		model.compile(optimizer='SGD',
						loss=tf.keras.losses.Hinge(),
						metrics=['accuracy'])


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
	return reward, moved


def swipe_left(state):
	"""
	Moves pieces to the left. Non-pure function.
	Returns: reward
	"""
	reward = 0
	moved = False
	for i in range(0, SIZE ** 2, SIZE):
		arange = range(i, SIZE + i)
		r, m = combiner(arange, state)
		reward += r
		moved = m or moved
	return reward, moved


def swipe_right(state):
	"""
	Moves pieces to the right. Non-pure function.
	Returns: reward
	"""
	reward = 0
	moved = False
	for i in range(SIZE - 1, SIZE ** 2, SIZE):
		arange = range(i, i - SIZE, -1)
		r, m = combiner(arange, state)
		reward += r
		moved = m or moved
	return reward, moved


def swipe_up(state):
	"""
	Moves pieces up. Non-pure function.
	Returns: reward
	"""
	reward = 0
	moved = False
	for i in range(0, SIZE, 1):
		arange = range(i, SIZE ** 2, SIZE)
		r, m = combiner(arange, state)
		reward += r
		moved = m or moved
	return reward, moved


def swipe_down(state):
	"""
	Moves pieces down. Non-pure function.
	Returns: reward
	"""
	reward = 0
	moved = False
	for i in range((SIZE - 1) * SIZE, SIZE ** 2, 1):
		arange = range(i, -1, -SIZE)
		r, m = combiner(arange, state)
		reward += r
		moved = m or moved
	return reward, moved


def evaluate(state, action):
	"""
	Returns the estimated value of a state
	Args:
		state:
		action:

	Returns:

	"""
	# Prediction is nested list
	return THETA[action].predict(tf.convert_to_tensor([state]))[0][0]


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
		reward, m = swipe_left(s_prime)
	elif action == 1:
		reward, m = swipe_right(s_prime)
	elif action == 2:
		reward, m = swipe_up(s_prime)
	elif action == 3:
		reward, m = swipe_down(s_prime)
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
	v_next = np.max([evaluate(s_dprime, i) for i in range(3)])
	THETA[action].fit(tf.convert_to_tensor([state]), tf.convert_to_tensor([reward + v_next]), verbose=0)


def get_moves(state):
	s1 = copy(state)
	s2 = copy(state)
	s3 = copy(state)
	s4 = copy(state)
	actions = []
	if swipe_left(s1)[1] * 1 == 1:
		actions.append(0)
	if swipe_right(s2)[1] * 1 == 1:
		actions.append(1)
	if swipe_up(s3)[1] * 1 == 1:
		actions.append(2)
	if swipe_down(s4)[1] * 1 == 1:
		actions.append(3)
	return actions


def play_game():
	learning_enabled = False
	score = 0
	# Init
	state = np.zeros(16)
	state = spawn_piece(state)
	# While not terminal
	while not is_terminal(state):
		# argmax
		max_val = -inf
		action = -1
		moves = get_moves(state)
		assert moves != []
		for i in moves:
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
	for y in range(50000):
		for x in range(5):
			try:
				ret_score = play_game()
				print("Game: ", x, " Score: ", ret_score)
			except BaseException as e:
				print(e)
				for i in range(len(THETA)):
					THETA[i].save("tf_model" + str(i) + ".h5")
				return
		print("Saving model at game "+str(x+y))
		for i in range(len(THETA)):
			THETA[i].save("tf_model" + str(i) + ".h5")


if __name__ == "__main__":
	main()
