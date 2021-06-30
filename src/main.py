from tensorforce import Agent
from tensorforce.execution import Runner

from board import Board
from random_agent import RandomAgent


def main():
    # Setup
    interactive = 0
    size = 4
    brd = Board(size)
    rand_ag = RandomAgent()

    if interactive == 1:
        brd.start_interactive()

    agent = Agent.create(agent='tensorforce', environment=Board, update=64, objective='policy_gradient',
                         reward_estimation=dict(horizon=20))

    runner = Runner(agent=agent, environment=Board, max_episode_timesteps=500)

    runner.run(num_episodes=200)


# brd.update_graphics()


if __name__ == "__main__":
    main()
