"""Utility classes and methods for turtles
to keep turtles.py clean
clean turtles
"""


class Direction:
    """For states and state transitioning
    """
    def __init__(self, name, key, transitions):
        """Initially a direction only has a name
        Arguments:
          - name (str): name of the direction
          - key (int or None): int associated with the gamepad key of this direction
          - transitions (dict): <Direction objects> with associated probabilities as values
        """
        self.name = name
        self.key = key
        self.transitions = transitions

    def update_transitions(self, name, probability):
        """Since not all connected states might be defined at initialization
        this method sets the connected states after initialization

        this method updates the transitions dict

        Arguments:
          - name (str): name of <Direction obj>
          - probability (int): probability, so should be between 0 - 100
        """
        self.transitions[name] = probability
