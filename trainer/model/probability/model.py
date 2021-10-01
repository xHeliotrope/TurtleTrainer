from dataclasses import dataclass
from trainer.model.base import Direction

class ProbabilityException(Exception):
    """Raised when a set of probabilities does not add up to 1 
    """
    pass

@dataclass
class ProbabilityNode:
    probability_start: int
    probability_end: int


class ProbabilitySet:
    def __init__(self, direction_probabilities):
        self.probabilities = []

        print(direction_probabilities)
        if (probability_sum := sum((d[1] for d in direction_probabilities))) != 100:
            raise ProbabilityException(f"Sum of probabilities are off by {100 - probability_sum}")

        probability_start = 0
        for value in direction_probabilities:
            self.probabilities.append(
                ProbabilityNode(
                    probability_start=probability_start,
                    probability_end=probability_start + value[1]
                )
            )
            probability_start += value[1]

    def get_button_index(self, sample_probability):
        if not sample_probability:
            raise ProbabilityException(f"Probability {sample_probability} must be non-zero")
        for index, probability_node in enumerate(self.probabilities):
            if probability_node.probability_start <= sample_probability <= probability_node.probability_end:
                return index

        raise Exception(f"Probability to change directions - {sample_probability} didn't fall within given probability ranges")
