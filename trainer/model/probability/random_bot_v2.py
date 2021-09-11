"""V2 of the Random Bot - a bit more Object-Oriented and testable
"""
import numpy as np
from gym import wrappers

from trainer.model.base import Bot
from trainer.model.base import Button
from trainer.model.base import Direction
from trainer.model.probability import ProbabilitySet


NULL_ACTION = np.zeros(9, dtype=np.int8)


class RandomBotV2(Bot):
    """Random Bot V2
    """
    def __init__(self, env, file_handler, action, attribute_list):
        super().__init__(env, 0, file_handler)
        self.action = action
        self.attribute_list = attribute_list

    def generate_transitions(self):
        """take a list of attributes and turn them into sets of buttons /
        probabilities
        """
        for attribute in self.attribute_list:
            pass

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
