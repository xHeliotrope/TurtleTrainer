import unittest

import pytest
import retro

from trainer.genetic.strategy import random_tuple
from trainer.genetic.strategy import end_weighted_probability
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

    def test_create_probability_set(self):
        moves = [
            (Direction('right', 7), 23),
            (Direction('left', 6), 44),
            (Direction(None,  None), 33)
        ]
        probability_set = ProbabilitySet(moves)
        assert type(probability_set) == ProbabilitySet
        assert type(probability_set.probabilities[0].direction) == Direction
        assert probability_set.probabilities[0].probability_start == 0
        assert probability_set.probabilities[0].probability_end == 23
        assert probability_set.probabilities[1].probability_start == 23
        assert probability_set.probabilities[1].probability_end == 67
        assert probability_set.probabilities[2].probability_start == 67
        assert probability_set.probabilities[2].probability_end == 100

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

    def test_genetic_algorithm_random_attribute_probabilities(self):
        """correctly creating attributes for genetic algorithm
        """
        attribute_sum = 0
        attributes = random_tuple(3, attribute_sum)
        assert attribute_sum == sum(attributes)

        attribute_sum = 1
        attributes = random_tuple(3, attribute_sum)
        assert attribute_sum == sum(attributes)

        #my_set = set()
        #counts = {
        #    str((1,0,0)): 0,
        #    str((0,1,0)): 0,
        #    str((0,0,1)): 0,
        #}
        #for x in range(300):
        #    attributes = random_tuple(3, attribute_sum)
        #    counts[str(attributes)] += 1
        #raise Exception(str(counts))


        attribute_sum = 100
        attributes = random_tuple(3, attribute_sum)
        assert attribute_sum == sum(attributes)

    def test_double_end_weighted_probability(self):
        attribute_sum = 1
        attributes = end_weighted_probability(3, attribute_sum)
        assert attribute_sum == sum(attributes)

        attribute_sum = 0
        attributes = end_weighted_probability(3, attribute_sum)
        assert attribute_sum == sum(attributes)

        attribute_sum = 100
        attributes = end_weighted_probability(3, attribute_sum)
        assert attribute_sum == sum(attributes)
