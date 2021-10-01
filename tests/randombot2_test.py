import unittest

import pytest
import retro

from trainer.handler import FileHandler
from trainer.handler import game_name
from trainer.model.base import Direction
from trainer.model.base import Button
from trainer.model.probability.model import ProbabilityException
from trainer.model.probability.random_bot_v2 import RandomBotV2


class RandomBot2Test(unittest.TestCase):
    """The RandomBot functions
    """
    def test_create_randombot(self):
        fh = FileHandler()
        env = retro.make(game=game_name, record='./' + fh.root_path)
        button_probs = ((1, 1), (2, 2), (3, 3))
        with pytest.raises(ProbabilityException) as excinfo:
            RandomBotV2(env, fh, (button_probs, button_probs, button_probs))
        assert '94' in str(excinfo.value)

    def test_create_env(self):
        fh = FileHandler()
        env = retro.make(game=game_name, record='./' + fh.root_path)
        states = (1, 33, 66)


        jump_attack = (
            (1, 34),
            (2, 33),
            (None, 33)
        )
        left_right = (
            (3, 33),
            (4, 33),
            (None, 34)
        )
        up_down = (
            (5, 33),
            (6, 33),
            (None, 34)
        )
        transitions = (
            jump_attack,
            left_right,
            up_down,
        )
        bot = RandomBotV2(env, fh, transitions)
        first_probability_set = bot.transitions[0]
        second_probability_set = bot.transitions[1]
        third_probability_set = bot.transitions[2]
        assert first_probability_set.get_button_index(27) is 0
        assert second_probability_set.get_button_index(55) is 1
        assert third_probability_set.get_button_index(27) is 0
