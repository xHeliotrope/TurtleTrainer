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
    =======================================
    This turtle has a probability (non-zero integer)
    of transitioning from on state to another
    (e.g. 'moving right' to 'moving left' 
    or 
    'jumping' to 'moving right and down')

    not very sophisticated,
    but the rewards are concrete and comparable (game score)
    which make this a candidate for use in a genetic algorithm
    """
    GAMEPAD_DIRS = {
        "vertical": {
            "up": 4,
            "down": 5,
            "vert_None": None
        },
        "horizontal": {
            "left": 6,
            "right": 7,
            "horiz_None": None
        }
    }

    def __init__(self, file_handler, transitions={}, default_cooldowns={'jump': 10, 'attack': 10}, directions={'4':0,'5':0,'6':0,'7':0}, **kwargs):
        """initialize the Static Probability Bot

        Arguments:
          - cooldowns (dict): cooldowns used after certain actions (can prevent special attack)
          - file_handler (<file_handler.FileHandler obj>): used for saving the actions/rewards to a txt file
          - transitions (dict): for registering all of the directions and evaluating how to move
                                based on the probilities defined in the associated Direction object
          - directions (dict): dict of `4`, `5`, `6` and `7` keys as `1` or `0` values
                               keys are the index of (`up`, `down`, `left`, `right` gamepad keys)
          - **kwargs (dict): not required params (direction/attack/jump probabilities)
        """
        # initial reward is 0
        super().__init__(0, file_handler)
        # setup the cooldowns
        self.cooldowns = {}
        self.transitions = transitions
        self.default_cooldowns = default_cooldowns
        for key, value in default_cooldowns.items():
            self.cooldowns[key] = value

        self.directions = directions

        self.to_attack = 5
        self.to_jump = 20
        if "attribute_list" in kwargs:
            self.update_directions(kwargs["attribute_list"])

    def update_directions(self, attribute_list):
        """Takes a list of attributes from deap
        and creates the necessary state transition variables
        for the StaticProbabilityTurtle

        Arguments:
          - (attribute_list): list of 0-100 probabilities for state transitions (e.g. up to down)

        Returns:
          - (dict): kwargs to be fed into StaticProbabilityTurtle constructor
        """
        jump_and_attack = attribute_list.pop(0)
        less_than_fifty = 0
        if jump_and_attack[0] < 50:
            less_than_fifty = jump_and_attack[0]
        else:
            less_than_fifty = jump_and_attack[1]

        self.to_jump = {'start': 0, 'end': less_than_fifty}
        self.to_attack = {'start': less_than_fifty, 'end':randint(less_than_fifty, 100)}
        print(self.to_jump)
        print(self.to_attack)

        for direction_set, directions in self.GAMEPAD_DIRS.items():
            related_directions = list(directions.keys())
            # this is needed so that the probabilities form a range
            for direction_name, direction_key in directions.items():
                new_direction = Direction(direction_name, direction_key)
                base_probability = 0
                for index, probability in enumerate(attribute_list.pop()):
                    new_direction.update_transitions(
                        related_directions[index], 
                        {
                            'start': base_probability, 
                            'end': base_probability + probability - 1
                        }
                    )

                    # update the base value for the next range
                    base_probability = base_probability + probability
                self.transitions[new_direction.name] = new_direction


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

    def compare_transition(self, direction_one, direction_two, number):
        greater_than = self.transitions[direction_one].transitions[direction_two]['start'] <= number
        less_than = self.transitions[direction_one].transitions[direction_two]['end'] >= number
        in_range = greater_than and less_than
        return in_range


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
            if self.compare_transition('right', 'left', random_number):
                self.switch_direction('7', '6')
            elif self.compare_transition('right', 'horiz_None', random_number):
                self.switch_direction('7', None)

        elif self.directions['6']:
            if self.compare_transition('left', 'right', random_number):
                self.switch_direction('6', '7')
            elif self.compare_transition('left', 'horiz_None', random_number):
                self.switch_direction('6', None)

        else:
            if self.compare_transition('horiz_None', 'left', random_number):
                self.switch_direction(None, '6')
            if self.compare_transition('horiz_None', 'right', random_number):
                self.switch_direction(None, '7')


        # (possibly) switch from up, down or None
        if self.directions['4']:
            if self.compare_transition('up', 'down', random_number):
                self.switch_direction('4', '5')
            elif self.compare_transition('up', 'vert_None', random_number):
                self.switch_direction('4', None)

        elif self.directions['5']:
            if self.compare_transition('down', 'up', random_number):
                self.switch_direction('5', '4')
            elif self.compare_transition('down', 'vert_None', random_number):
                self.switch_direction('5', None)

        else:
            if self.compare_transition('vert_None', 'down', random_number):
                self.switch_direction(None, '4')
            elif self.compare_transition('vert_None', 'up', random_number):
                self.switch_direction(None, '5')


        # attack when the `jump` cooldown is inactive
        if self.to_attack['start'] <= random_number <= self.to_attack['end'] and self.cooldowns['jump'] <= 0:
            action[0] = 1
            # prevent special attacks
            self.cooldowns['attack'] = 10

        # jump when the `attack` cooldown is inactive
        if self.to_jump['start'] <= random_number <= self.to_jump['end'] and self.cooldowns['attack'] <= 0:
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
        no_change = 0
        while not done:
            # random integer used for state-transition decision making
            random_int = randint(0, 100)
            # base action is to do nothing (all buttons on keypad are zero)
            action = np.zeros(9, dtype=np.int8)
            # determine next action (uses previous state information of direction)
            action = self.next_action(action, random_int)
            # take an action in the environment, and get the environmental info from that step
            _obs, _rew, done, _info = env.step(action)
            if not _rew:
                no_change +=1
                if no_change > 10000:
                    done = True
            else:
                no_change = 0
            score += _rew

        self.reward = score

