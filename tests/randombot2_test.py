import unittest

import pytest
import retro

from trainer.handler import FileHandler
from trainer.handler import game_name
from trainer.model.base import Direction
from trainer.model.probability.random_bot_v2 import RandomBotV2


class RandomBotTest(unittest.TestCase):
    """The RandomBot functions
    """
    def test_create_randombot(self):
        fh = FileHandler()
        env = retro.make(game=game_name, record='./' + fh.root_path)
        bot = RandomBotV2(env, fh, {}, attribute_list = [])
        assert type(bot) == RandomBotV2

    def test_create_env(self):
        fh = FileHandler()
        env = retro.make(game=game_name, record='./' + fh.root_path)
        states = (1, 33, 66)
        transitions = [(1,99), states, states, states, states, states, states]
        bot = RandomBotV2(env, fh, {}, attribute_list=transitions)
