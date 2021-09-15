from dataclasses import dataclass
from trainer.model.base import Direction

class ProbabilityException(Exception):
    """Raised when a set of probabilities does not add up to 1 
    """
    pass

@dataclass
class ProbabilityNode:
    direction: Direction
    probability_start: int
    probability_end: int


class ProbabilitySet:
    def __init__(self, direction_probabilities):
        self.probabilities = []
        probability_sum = sum(n[1] for n in direction_probabilities) 

        # assert valid probabilities
        if probability_sum != 100:
            raise ProbabilityException(f"Sum of probabilities are off by {100 - probability_sum}")

        probability_start = 0
        for index, node in enumerate(direction_probabilities):
            self.probabilities.append(
                ProbabilityNode(
                    direction=node[0],
                    probability_start=probability_start,
                    probability_end=probability_start + node[1]
                )
            )
            probability_start += node[1]

    def get_button(self, sample_probability):
        if not sample_probability:
            raise ProbabilityException(f"Probability {sample_probability} must be non-zero")
        for probability_node in self.probabilities:
            if probability_node.probability_start <= sample_probability <= probability_node.probability_end:
                return probability_node.direction
        raise Exception(f"Probability to change directions - {sample_probability} didn't fall within given probability ranges")
