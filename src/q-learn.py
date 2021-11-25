import random
from copy import deepcopy, copy
from math import inf

import numpy as np
import tensorflow as tf
from tensorflow import keras

# Learning rate
ALPHA = 0.001
# Size of the game board
SIZE = 4
# Value vectors for q-learning
THETA = None


def setup(parametrize=False):
    if parametrize:
        THETA = np.array(
            [np.random.random((16,)), np.random.random((16,)), np.random.random((16,)), np.random.random((16,))])
    else:
        # Use tf models instead
        try:
            # Load models from disk if possible
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
                model.compile(optimizer='SGD', loss=tf.keras.losses.Hinge(), metrics=['accuracy'])


def evaluate(state, action):
    """
    Returns the estimated value of a state-action pair
    Args:
        state: Game state
        action: Action to be taken from the state

    Returns: Estimated value

    """
    # Prediction is nested list
    return THETA[action].predict(tf.convert_to_tensor([state]))[0][0]


def compute_afterstate(state, action):
    """
    Computes the afterstate (before random piece spawn). Pure function.
    Args:
        state: Game state
        action: Action to execute (integer)

    Returns: Tuple of state after executing action and reward gained by action

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
    """
    Trains the value approximation function
    Args:
        state: Game state
        action: Action
        reward: Reward for taking action from state
        s_prime: State after action but before random tile generation
        s_dprime: Final state after action

    Returns: None

    """
    v_next = np.max([evaluate(s_dprime, i) for i in range(3)])
    THETA[action].fit(tf.convert_to_tensor([s_prime]), tf.convert_to_tensor([reward + v_next]), verbose=0)


def get_moves(state):
    """
    Checks which moves are available
    Args:
        state: Game state

    Returns: List of legal moves

    """
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
    """
    Plays the game. Can optionally enable training of the value function approximater
    Returns: Final score

    """
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
        # Train value approximater
        if learning_enabled:
            learn_evaluation(state, action, reward, s_prime, s_dprime)
        score += reward
        # Advance state
        state = s_dprime
    return score


def main():
    """
    This setup isn't exact to what was used to generate empirical results. Running this in its current state
    will take FOREVER (days or weeks).
    Returns: None

    """
    learning = False
    scores = np.zeros(10000)
    for x in range(10000):
        try:
            ret_score = play_game()
            print("Game: ", x, " Score: ", ret_score)
            scores[x] = ret_score
        except BaseException as er:
            print(er)
            if learning:
                for i in range(len(THETA)):
                    THETA[i].save("tf_model" + str(i) + ".h5")
            return
    print("Max: ", np.max(scores), " Min: ", np.min(scores), " Avg: ", np.average(scores))
    print("STDEV: ", np.std(scores), " Median: ", np.median(scores))
    if learning:
        # print("Saving model at game "+str(x))
        for i in range(len(THETA)):
            THETA[i].save("tf_model" + str(i) + ".h5")


if __name__ == "__main__":
    main()
