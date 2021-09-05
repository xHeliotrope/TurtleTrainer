"""Bot creation - regardless of learning method used (probability / neural net)
"""

class Bot:
    """base class for playing ninja turtles
    """
    def __init__(self, env, reward, file_handler):
        """
        Arguments:
          - env (<retro.retro_env.RetroEnv obj>): Open AI Retro Game Environment
          - reward (int): current reward value
          - file_handler (<FileHandler obj>): for saving game replays
        """
        self.env = env
        self.reward = reward
        self.file_handler = file_handler


class Direction:
    """For states and state transitioning
    """
    def __init__(self, name, key):
        """Initially a direction only has a name

        Arguments:
          - name (str): name of the direction
          - key (int or None): int associated with the gamepad key of this direction
        """
        self.name = name
        self.key = key
        self.transitions = {}

    def __repr__(self):
        return f'Direction {self.name}'

    def update_transitions(self, name, probability):
        """
        Arguments:
          - name (str): name of <Direction obj>
          - probability (dict): has `start` and `end` keys, creating a numeric range
                                which represent a probability
                                so {'start': 13, 'end': 23} would be a 10 percent chance
        """
        self.transitions[name] = probability
