"""
file: main.py
copyright: Owen Siljander 2021
"""

import cProfile, pstats
from controller import Controller


def main():
    c = Controller()
    # c.run_interactive()
    c.run_agent(agent_type='DRAgent', graphics=True)

"""
===== Old Main Fragment =====

def main():
    # Setup
    interactive = 0
    size = 4
    brd = Board(size, graphics=0)
    rand_ag = RandomAgent()

    if interactive == 1:
        brd.start_interactive()

    agent = Agent.create(agent='tensorforce', environment=Board, update=64, objective='policy_gradient',
                         reward_estimation=dict(horizon=20))

    runner = Runner(agent=agent, environment=Board, max_episode_timesteps=500)

    runner.run(num_episodes=200)

"""

if __name__ == "__main__":
    main()
