"""
for reference, the actions agents use for NES gamepad are:
  0 - "b"
  1 - "null"
  2 - "select"
  3 - "start"
  4 - "up"
  5 - "down"
  6 - "left"
  7 - "right"
  8 - "a"
"""
from random import randint

import numpy as np

from turtle_utils import Direction

class Turtle:
    """base class for bots to be run using the 'deap' genetic algorithm library
    """
    def __init__(self, reward, file_handler):
        """every turtle needs a reward
        """
        self.reward = reward
        self.file_handler = file_handler

class StaticProbabilityTurtle(Turtle):
    """hard coded probability-based agent
    probability checks could be standardized
    sometimes probabilities are evaluated if a number is less than a random number
    other times its if a number modulo another number is 0
    not very sophisticated, but the state transition numbers are configurable
    and the rewards are concrete
    which make this a good candidate for use in a genetic algorithm
    """
    def __init__(self, file_handler, default_cooldowns={'jump': 10, 'attack': 10}, directions={'4':0,'5':0,'6':0,'7':0}, **kwargs):
        """initialize the Static Probability Bot

        Arguments:
          - cooldowns (dict): cooldowns used after certain actions (can prevent special attack)
          - file_handler (<file_handler.FileHandler obj>): used for saving the actions/rewards to a txt file
          - directions (dict): dict of `4`, `5`, `6` and `7` keys as `1` or `0` values
                               keys are the index of (`up`, `down`, `left`, `right` gamepad keys)
          - **kwargs (dict): not required params (direction/attack/jump probabilities)
        """
        # initial reward is 0
        super().__init__(0, file_handler)
        # setup the cooldowns
        self.cooldowns = {}
        self.default_cooldowns = default_cooldowns
        for key, value in default_cooldowns.items():
            self.cooldowns[key] = value

        self.directions = directions

        # this is a template for the horizontal directions
        # to use for defining state transitions
        self.horizontal_transition_probability_template = {
            'right': 0,
            'left': 0,
            'horiz_None': 0
        }
        self.vertical_transition_probability_template = {
            'up': 0,
            'down': 0,
            'vert_None': 0
        }

        self.to_attack = 5
        self.to_jump = 20

        if 'horizontal_transitions' in kwargs:
            self.horizontal_transitions = kwargs['horizontal_transitions']
        if 'vertical_transitions' in kwargs:
            self.vertical_transitions = kwargs['vertical_transitions']
        if 'to_jump' in kwargs:
            self.to_jump = kwargs['to_jump']
        if 'to_attack' in kwargs:
            self.to_attack = kwargs['to_attack']

    @staticmethod
    def prepare_kwargs(attribute_list):
        """Takes a list of attributes from deap
        and creates the necessary state transition variables in
        the constructor for the StaticProbabilityTurtle

        Arguments:
          - (attribute_list): list of 0-100 probabilities for state transitions (e.g. up to down)

        Returns:
          - (dict): kwargs to be fed into StaticProbabilityTurtle constructor
        """
        the_kwargs = {}
        return the_kwargs


    def switch_direction(self, current, future):
        """switch directions from current to future
        e.g. go from going `right` to going `left` or going `up` to `neither`

        its possible to go from a direction to no direction (None is allowed)
        
        Arguments:
          - current (int or None): direction to stop going
          - future (int or None): direction to start going 
        """
        if current:
            self.directions[current] = 0
        if future:
            self.directions[future] = 1

    def next_action(self, action, random_number):
        """calculates next action to take,
        from previous action state

        Arguments:
          - action (numpy array [int8]): 9 element numpy array of NES gamepad actions
          - random_number (int): random number used to evaluate next actions

        Returns:
          - (numpy array [int8]): 9 element numpy array of NES gamepad actions
        """
        # decrement the jump and attack cooldowns
        self.cooldowns['jump'] -= 1
        self.cooldowns['attack'] -= 1
        
        # (possibly) switch from right to left or left to right
        if self.directions['7']:
            if random_number % self.horizontal_transitions['right']['to_left'] == 0:
                # switch from right to left
                self.switch_direction('7', '6')
        else:
            if random_number % self.horizontal_transitions['left']['to_right'] == 0:
                # switch from left to right
                self.switch_direction('6', '7')

        # (possibly) switch from up, down or None
        if self.directions['4']:
            if random_number < self.vertical_transitions['up']['to_down']:
                # switch from up to down 
                self.switch_direction('4', '5')
            elif random_number < self.vertical_transitions['up']['to_None']:
                # switch from up to None
                self.switch_direction('4', None)
        elif self.directions['5']:
            if random_number < self.vertical_transitions['down']['to_up']:
                # switch from down to up
                self.switch_direction('5', '4')
            elif random_number < self.vertical_transitions['down']['to_None']:
                # switch from down to None
                self.switch_direction('5', None)
        else:
            if random_number < self.vertical_transitions['None']['to_up']:
                # switch from None to up
                self.switch_direction(None, '4')
            elif random_number < self.vertical_transitions['None']['to_down']:
                # switch from None to down
                self.switch_direction(None, '5')

        # attack like 5% of the time, when the `jump` cooldown is inactive
        if random_number < self.to_attack and self.cooldowns['jump'] <= 0:
            action[0] = 1
            # prevent special attacks
            self.cooldowns['attack'] = 10

        # attack like 20% of the time, when the `attack` cooldown is inactive
        if random_number < self.to_jump and self.cooldowns['attack'] <= 0:
            action[8] = 1
            self.cooldowns['jump'] = 10

        # set next action to possibly-updated directions
        for key, value in self.directions.items():
            action[int(key)] = value

        return action

    def run_simulation(self, env):
        """run the simulation, and log the states

        Arguments:
          - env (<retro.retro_env.RetroEnv obj>): Open AI Retro Game Environment
        """
        # boolean value denoting whether the bot has died yet or not (ends the simulation)
        done = False

        score = 0
        while not done:
            # random integer used for state-transition decision making
            random_int = randint(0, 100)
            # base action is to do nothing (all buttons on keypad are zero)
            action = np.zeros(9, dtype=np.int8)
            # determine next action (uses previous state information of direction)
            action = self.next_action(action, random_int)
            # take an action in the environment, and get the environmental info from that step
            _obs, _rew, done, _info = env.step(action)
            score += _rew

        self.reward = score

