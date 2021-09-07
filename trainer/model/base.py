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


class Button:
    """For states and state transitioning
    """
    def __init__(self, name, key):
        """Initially a button only has a name

        Arguments:
          - name (str): name of the button
          - key (int or None): int associated with the gamepad key of this button
        """
        self.name = name
        self.key = key

    def __repr__(self):
        return f'Button {self.name}'


class Direction(Button):

    def __init__(self, name, key):
        super().__init__(name, key)
        self.transitions = {}

    def update_transitions(self, name, probability):
        """
        Arguments:
          - name (str): name of <Direction obj>
          - probability (dict): has `start` and `end` keys, creating a numeric range
                                which represent a probability
                                so {'start': 13, 'end': 23} would be a 10 percent chance
        """
        self.transitions[name] = probability

    def __repr__(self):
        return f'Direction {self.name}'
