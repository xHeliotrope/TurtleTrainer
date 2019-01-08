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


class Turtle:
    """base class for bots to be run using the 'deap' genetic algorithm library
    """
    def __init__(self, reward):
        """every turtle needs a reward
        """
        self.reward = reward

class StaticProbabilityTurtle(Turtle):
    """hard coded probability-based agent
    probability checks could be standardized
    sometimes probabilities are evaluated if a number is less than a random number
    other times its if a number modulo another number is 0
    not very sophisticated, but the state transition numbers are configurable
    which makes this a good candidate for use in a genetic algorithm
    """
    def __init__(self, cooldowns, file_handler, directions={'4':0,'5':0,'6':0,'7':0}, **kwargs):
        """initialize the Static Probability Bot

        Arguments:
          - cooldowns (dict): cooldowns used after certain actions (can prevent special attack)
          - file_handler (<file_handler.FileHandler obj>): used for saving the actions/rewards to a txt file
          - directions (dict): dict of `4`, `5`, `6` and `7` keys as `1` or `0` values
                               keys are the index of (`up`, `down`, `left`, `right` gamepad keys)
          - **kwargs (dict): not required params (direction/attack/jump probabilities)
        """
        # initial reward is 0
        super().__init__(0)
        self.cooldowns = cooldowns
        self.file_handler = file_handler
        self.directions = directions
        # the following numbers are used to compute when to change direction or attack or jump 
        #   probabilities:
        #       - vertical:
        #           - up
        #               - 10% switch from up to down
        #               - 3% switch from up to None
        #               - 87% no change
        #           - down
        #               - 10% switch from down to up
        #               - 3% switch from down to None
        #               - 87% no change
        #           - None
        #               - 20% switch from None to up
        #               - 20% switch from None to down
        #               - 60% no change
        #       - horizontal:
        #           - left
        #               - 10% switch probability from right to left
        #               - 90% no change
        #           - left
        #               - 20% switch probability from left to right 
        #               - 80% no change
        #       - attack:
        #           - 5% of the time
        #       - jump:
        #           - 20% of the time

        self.horizontal_transitions = {
            'right': {
                'to_left': 20
            },
            'left': {
                'to_right': 10
            }
        }

        # theres probably a better way to do this,
        # but these probabilities are calculated in like a cumulative way
        # so if `to_down` is '5', that means random numbers 5 and under will 
        # trigger a direction change to `down`
        # and if `to_None is '10', that means random numbers 10 and under will
        # trigger a direction change to `None`
        # which means that although `to_down` and `to_None` are different values here,
        # they each have the same probability of occuring
        # since `to_down` will match numbers 0,1,2,3,4
        # and `to_None` will match numbers 5,6,7,8,9
        self.vertical_transitions = {
            'up': {
                'to_down': 5,
                'to_None': 10
            },
            'down': {
                'to_up': 5,
                'to_None': 10
            },
            'None': {
                'to_up': 5,
                'to_down': 10
            }
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

        print(action)
        return action

    def run_simulation(self, env):
        """run the simulation, and log the states

        Arguments:
          - env (<retro.retro_env.RetroEnv obj>): Open AI Retro Game Environment
        """
        # boolean value denoting whether the bot has died yet or not (ends the simulation)
        done = False

        while not done:
            # random integer used for state-transition decision making
            random_int = randint(0, 100)
            # base action is to do nothing (all button on keypad are zero)
            action = np.zeros(9, dtype=np.int8)
            # determine next action (uses previous state information of direction)
            action = self.next_action(action, random_int)
            # take an action in the environment, and get the environmental info from that step
            _obs, _rew, done, _info = env.step(action)
            # next 3 lines write the action that was taken and the reward from that action to a file
            state_info = np.append(action, _rew)
            state_str = str(state_info)
            self.file_handler.log_state(state_str)

        self.reward = _rew
