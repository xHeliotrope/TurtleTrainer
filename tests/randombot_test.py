import unittest

import pytest
import retro

from trainer.handler import FileHandler
from trainer.handler import game_name
from trainer.model.probability.random_bot import RandomBot
from trainer.model.probability.model import ProbabilitySet
from trainer.model.probability.model import ProbabilityException
from trainer.model.base import Direction


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

    def test_create_probability_set(self):
        moves = [
            (Direction('right', 7), 23),
            (Direction('left', 6), 44),
            (Direction(None,  None), 33)
        ]
        probability_set = ProbabilitySet(moves)
        assert type(probability_set) == ProbabilitySet
        assert type(probability_set.probabilities[0].direction) == Direction
        assert probability_set.probabilities[0].probability == 23
        assert probability_set.probabilities[1].probability == 44

    def test_create_probability_set_fails_on_invalid_probabilities(self):
        moves = [
            (Direction('right', 7), 23),
            (Direction('up', 7), 77),
            (Direction('left', 6), 44),
            (Direction(None,  None), 33)
        ]
        with pytest.raises(ProbabilityException) as excinfo:
            ProbabilitySet(moves)
        assert '-77' in str(excinfo.value)
