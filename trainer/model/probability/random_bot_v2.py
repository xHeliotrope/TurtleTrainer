"""V2 of the Random Bot - a bit more Object-Oriented and testable
"""
import numpy as np
from gym import wrappers

from trainer.model.base import Bot
from trainer.model.base import Button
from trainer.model.base import Direction
from trainer.model.probability import ProbabilitySet

up_down = {
    4: 0,  # up
    5: 0,  # down
    None: 0,  # none
}

left_right = {
    6: 0,  # left
    7: 0,  # right
    None: 0,  # none
}

a_b = {
    0: 0,  # a
    8: 0,  # b
    None: 0,  # none
}

button_set = (a_b, left_right, up_down)


def apply_action_update(action, update):
    '''XOR the action and the update to get the updated action
    '''
    return [x ^ y for x, y in zip(action,  update)]

def get_next_action(action, updates):
    '''apply all updates to the current
    '''
    return reduce(lambda acc, ele: apply_action_update(acc, ele), action + updates)

def generate_update(active_indices):
    '''
    '''
    action = np.zeros(9, dtype=np.int8)
    for index in active_indices:
        action[index] = 1
    return action


class RandomBotV2(Bot):
    """Random Bot V2
    """
    def __init__(self, env, file_handler, direction_probabilities):
        super().__init__(env, 0, file_handler)
        self.action = np.zeros(9, dtype=np.int8)
        self.transitions = []

        assert len(direction_probabilities) == len(button_set)

        for index, value in enumerate(button_set):
            print(type(value), value, type(direction_probabilities[index]), direction_probabilities[index])
            self.transitions.append(ProbabilitySet(direction_probabilities[index]))

    def next_action(self):
        for transition in self.transition:
            pass

        return self.action

    def run_simulation(self):
        """run the simulation and log the states
        """
        # boolean value denoting whether the bot has died yet or not (ends the simulation)
        done = False

        score = 0
        no_change = 0
        self.env.reset()
        while not done:
            action = self.next_action()
            # take an action in the environment, and get the environmental info from that step
            _obs, _rew, done, _info = self.env.step(action)
            if not _rew:
                no_change += 1
                if no_change > 10000:
                    done = True
            else:
                no_change = 0
            score += _rew

        self.reward = score
