#!/usr/bin/env python3
import gym


def run():
    env = gym.make('MountainCar-v0')

    for episode in range(100):
        env.reset()
        state_pos = 0
        while 1:
            env.render()

            action = env.action_space.sample()
            state_pos = env.step(2)[0][1]
            if state_pos < 0:
                state = env.step(1)
            else:
                state = env.step(2)

            state_po = state[0][1]


if __name__ == '__main__':
    run()
