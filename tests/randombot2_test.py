import unittest

import pytest
import retro

from trainer.handler import FileHandler
from trainer.handler import game_name
from trainer.model.base import Direction
from trainer.model.base import Button
from trainer.model.probability.random_bot_v2 import RandomBotV2


class RandomBot2Test(unittest.TestCase):
    """The RandomBot functions
    """
    def test_create_randombot(self):
        fh = FileHandler()
        env = retro.make(game=game_name, record='./' + fh.root_path)
        bot = RandomBotV2(env, fh, {})
        assert type(bot) == RandomBotV2

    def test_create_env(self):
        fh = FileHandler()
        env = retro.make(game=game_name, record='./' + fh.root_path)
        states = (1, 33, 66)

        jump = Button('jump', 0)
        right = Direction('right', 3)
        up = Direction('up', 4)
        null_start_select = Direction('null_start_select', None)

        jump_attack = (
            (jump, 34),
            (Button('attack', 1), 33),
            (Button('null_jump_attack', None), 33)
        )
        left_right = (
            (Direction('left', 2), 33),
            (right, 33),
            (Direction('null_left_right', None), 34)
        )
        up_down = (
            (up, 33),
            (Direction('down', 5), 33),
            (Direction('null_up_down', None), 34)
        )
        select_start = (
            (Direction('select', 6), 0),
            (Direction('start', 7), 0),
            (null_start_select, 100)
        )
        transitions = (
            jump_attack,
            left_right,
            up_down,
            select_start
        )
        bot = RandomBotV2(env, fh, transitions)
        first_probability_set = bot.transitions[0]
        second_probability_set = bot.transitions[1]
        third_probability_set = bot.transitions[2]
        fourth_probability_set = bot.transitions[3]
        assert first_probability_set.get_button(27) is jump
        assert second_probability_set.get_button(55) is right
        assert third_probability_set.get_button(27) is up
        assert fourth_probability_set.get_button(66) is null_start_select
