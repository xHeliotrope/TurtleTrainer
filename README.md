# NES GAME BOT


Throwing some machine learning at retro gaming.

So far there are two bots:

+ Probability Bot
+ DeepQ Bot - courtesy [transedward](https://github.com/transedward/pytorch-dqn)

These bots attempt to complete games of Teenage Mutant Ninja Turtles.
The plan is to gain efficiency at beating the levels or retain some measure of skill over time.

The probability bot is simple - it creates a set of probabilities that a bot will go from one action to another.
For example, from moving left to moving down. Or from standing still to attacking.
A bunch of turtle bots are generated with their own probabilities and then each one plays the game.
All of the scores and replays are recorded and the "best" bots are the ones that achieve the highest scores.

The DeepQ Bot is ~99% lifted from another Deep Q game playing algorithm.
The training code can be used to generate models/hyperparameters.
[Deep Q Learning](https://en.wikipedia.org/wiki/Q-learning#Deep_Q-learning)


#### Still in the works
 # Wavelets/FFTs for feature detection to feed as input to train the DeepQ Bot

#### TODOs:
 - [ ] use a wrapper for retro-gym instead of customizing retro-gym
 - [ ] create a docker container/possible swarm for parallel genetic ops
 - [ ] figure out whats creating 2 videos in retro-gym
 - [ ] register games instead of placing them in virtualenv
 - [ ] create tutorial
 - [ ] update jupyter notebook comparing genetic and RL methods


