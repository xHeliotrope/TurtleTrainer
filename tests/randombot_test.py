import unittest

import pytest
import retro

from trainer.genetic.strategy import end_weighted_probability
from trainer.genetic.strategy import random_tuple
from trainer.genetic.strategy import uniform_probability
from trainer.handler import FileHandler
from trainer.handler import game_name
from trainer.model.base import Direction
from trainer.model.probability.random_bot import RandomBot
from trainer.model.probability.model import ProbabilitySet
from trainer.model.probability.model import ProbabilityException


class RandomBotTest(unittest.TestCase):
    """The RandomBot functions
    """
    def test_create_randombot(self):
        fh = FileHandler()
        env = retro.make(game=game_name, record='./' + fh.root_path)
        bot = RandomBot(env, fh, {})
        assert type(bot) == RandomBot

    def test_create_env(self):
        fh = FileHandler()
        env = retro.make(game=game_name, record='./' + fh.root_path)
        bot = RandomBot(env, fh, {})
        states = (1, 33, 66)
        transitions = [(1,99), states, states, states, states, states, states]
        bot.update_directions(transitions)
        assert bot.to_jump["start"] == 0
        assert bot.to_jump["end"] >= 1

