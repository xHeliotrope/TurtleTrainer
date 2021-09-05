from dataclasses import dataclass
from trainer.model.base import Direction

class ProbabilityException(Exception):
    """Raised when a set of probabilities does not add up to 1 
    """
    pass

@dataclass
class ProbabilityNode:
    direction: Direction
    probability: int


class ProbabilitySet:
    def __init__(self, direction_probabilities):
        self.probabilities = []
        probability_sum = sum(n[1] for n in direction_probabilities) 

        # assert valid probabilities
        if probability_sum != 100:
            raise ProbabilityException(f"Sum of probabilities are off by {100 - probability_sum}")

        for index, node in enumerate(direction_probabilities):
            self.probabilities.append(ProbabilityNode(node[0], node[1]))

