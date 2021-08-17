from dataclasses import dataclass
from trainer.model.base import Direction

@dataclass
class ProbabilityNode:
    direction: Direction
    probability: float


class MoveProbabilitySet:
    # implement to make safe
    #def __new__(cls, *args, **kwargs):
    #    raise RuntimeError('%s should not be instantiated' % cls)

    def __init__(self, directions, *args):
        self.direction = direction
        self.probability_length = 0
        for index, probability_tuple in enumerate(*args):
            node = ProbabilityNode(n[0], n[1])
            setattr(self, f'p_{index}', node)
            self.probability_length += 1

