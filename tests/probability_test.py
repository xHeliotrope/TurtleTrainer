import unittest

import pytest

from trainer.genetic.strategy import end_weighted_probability
from trainer.genetic.strategy import random_tuple
from trainer.genetic.strategy import uniform_probability
from trainer.model.base import Direction
from trainer.model.probability.model import ProbabilitySet
from trainer.model.probability.model import ProbabilityException


class ProbabilityTest(unittest.TestCase):
    """The RandomBot functions
    """
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


