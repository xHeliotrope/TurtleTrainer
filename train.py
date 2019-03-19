import sys
import random

from collections import namedtuple
from itertools import count

import numpy as np

import gym
from gym import wrappers
import retro

import torch
from torch import autograd

from file_handler import FileHandler
from model import neural_turtle
from model import utils

game_name = 'TeenageMutantNinjaTurtlesIIITheManhattanProject-Nes'
game_meta = '-1Player.Leo.Level1-000000'

OptimizerSpec = namedtuple("OptimizerSpec", ["constructor", "kwargs"])

#####
# VARIABLES FOR STUFF
#####


Statistic = {
    "mean_episode_rewards": [],
    "best_mean_episode_rewards": []
}
USE_CUDA = torch.cuda.is_available()
LEARNING_RATE = 0.00025
ALPHA = 0.95
EPS = 0.01
# learning_starts = 50000
learning_starts = 1000
learning_freq = 4
batch_size=32
gamma=0.99
num_timesteps = int(4e7)
exploration_schedule = utils.LinearSchedule(1000000, 0.1)
target_update_freq = 10000

optimizer_spec = OptimizerSpec(
    constructor=torch.optim.RMSprop,
    kwargs=dict(lr=LEARNING_RATE, alpha=ALPHA, eps=EPS),
)

def stopping_criterion(env, t):
    return t >= num_timesteps

class Variable(autograd.Variable):
    def __init__(self, data, *args, **kwargs):
        if USE_CUDA:
            data = data.cuda()
        super(Variable, self).__init__(data, *args, **kwargs)

# Construct an epsilon greedy policy with given exploration schedule
def select_epsilon_greedy_action(model, obs, t):
    dtype = torch.cuda.FloatTensor if torch.cuda.is_available() else torch.FloatTensor
    sample = random.random()
    num_actions = 9
    eps_threshold = exploration_schedule.value(t)
    if sample > eps_threshold:
        print('pre model_obs shape == >', obs.shape)
        obs = torch.from_numpy(obs).type(dtype).unsqueeze(0) / 255.0
        # Use volatile = True if variable is only used in inference mode, i.e. don’t save the history
        print('post model_obs shape == >', obs.shape)
        stuff = model(Variable(obs)).data.max(1)[1].cpu()
        print('last obs_shape ==> ', stuff.shape)
        return stuff
    else:
        randobs = torch.IntTensor([[random.randrange(num_actions)]])  
        print("randobs shape ==> ", randobs.shape)
        return randobs

def main():
    frame_history_len = 4
    dtype = torch.cuda.FloatTensor if torch.cuda.is_available() else torch.FloatTensor

    file_handl = FileHandler(file_number=random.randint(0, 10000000))
    file_handl.create_video_dir()
    env = retro.make(game=game_name, record='./' + file_handl.root_path)
    # env = wrappers.Monitor(env, './recordings', force=True)

    img_h, img_w = env.observation_space.shape

    input_arg = frame_history_len
    num_actions = env.action_space.n

    q_func = neural_turtle.DeepQTurtle


    Q = q_func(input_arg, num_actions).type(dtype)
    target_Q = q_func(input_arg, num_actions).type(dtype)

    optimizer = optimizer_spec.constructor(Q.parameters(), **optimizer_spec.kwargs)

    # replay_buffer = utils.ReplayBuffer(size=1000, frame_history_len=frame_history_len)
    replay_buffer = utils.ReplayBuffer(size=100000, frame_history_len=frame_history_len)


    ###############
    # RUN ENV     #
    ###############
    num_param_updates = 0
    mean_episode_reward = -float('nan')
    best_mean_episode_reward = -float('inf')
    last_obs = env.reset()
    LOG_EVERY_N_STEPS = 10000

    for t in count():
        ### Check stopping criterion
        if stopping_criterion is not None and stopping_criterion(env, t):
            break

        ### Step the env and store the transition
        # Store lastest observation in replay memory and last_idx can be used to store action, reward, done
        last_idx = replay_buffer.store_frame(last_obs)
        # encode_recent_observation will take the latest observation
        # that you pushed into the buffer and compute the corresponding
        # input that should be given to a Q network by appending some
        # previous frames.
        recent_observations = replay_buffer.encode_recent_observation()

        # Choose random action if not yet start learning
        if t > learning_starts:
            action = select_epsilon_greedy_action(Q, recent_observations, t)
            poss_act = np.zeros(num_actions)
            poss_act[action] = 1
            action = poss_act
        else:
            action = random.randrange(num_actions)
            poss_act = np.zeros(num_actions)
            poss_act[action] = 1
            action = poss_act
        # Advance one step
        obs, reward, done, _ = env.step(action)
        # clip rewards between -1 and 1
        reward = max(-1.0, min(reward, 1.0))
        # Store other info in replay memory
        replay_buffer.store_effect(last_idx, action, reward, done)
        # Resets the environment when reaching an episode boundary.
        if done:
            obs = env.reset()
        last_obs = obs

        ### Perform experience replay and train the network.
        # Note that this is only done if the replay buffer contains enough samples
        # for us to learn something useful -- until then, the model will not be
        # initialized and random actions should be taken
        if (t > learning_starts and
                t % learning_freq == 0 and
                replay_buffer.can_sample(batch_size)):
            # Use the replay buffer to sample a batch of transitions
            # Note: done_mask[i] is 1 if the next state corresponds to the end of an episode,
            # in which case there is no Q-value at the next state; at the end of an
            # episode, only the current state reward contributes to the target
            obs_batch, act_batch, rew_batch, next_obs_batch, done_mask = replay_buffer.sample(batch_size)
            # Convert numpy nd_array to torch variables for calculation
            obs_batch = Variable(torch.from_numpy(obs_batch).type(dtype) / 255.0)
            act_batch = Variable(torch.from_numpy(act_batch).long())
            rew_batch = Variable(torch.from_numpy(rew_batch))
            next_obs_batch = Variable(torch.from_numpy(next_obs_batch).type(dtype) / 255.0)
            not_done_mask = Variable(torch.from_numpy(1 - done_mask)).type(dtype)

            if USE_CUDA:
                act_batch = act_batch.cuda()
                rew_batch = rew_batch.cuda()

            # Compute current Q value, q_func takes only state and output value for every state-action pair
            # We choose Q based on action taken.
            # return Q, obs_batch, act_batch
            current_Q_values = Q(obs_batch).gather(1, act_batch.unsqueeze(1))
            # Compute next Q value based on which action gives max Q values
            # Detach variable from the current graph since we don't want gradients for next Q to propagated
            target_batchz = target_Q(next_obs_batch)
            # print("targetQ(next_obs_batch).shape ==> ", target_batchz.shape)
            next_max_q = target_batchz.detach().max(1)[0]
            # print("next_max_q ==> ", next_max_q.shape)
            next_Q_values = not_done_mask * next_max_q
            # Compute the target of the current Q values
            target_Q_values = rew_batch + (gamma * next_Q_values)
            # Compute Bellman error
            bellman_error = target_Q_values - current_Q_values
            # clip the bellman error between [-1 , 1]
            clipped_bellman_error = bellman_error.clamp(-1, 1)
            # Note: clipped_bellman_delta * -1 will be right gradient
            d_error = clipped_bellman_error * - 1.0
            # Clear previous gradients before backward pass
            optimizer.zero_grad()

            # run backward pass
            # print("error data size ==> ", d_error.data.size())
            # print("error data (unsqueezed(1)) ==> ", d_error.data.unsqueeze(1).size())
            current_Q_values.backward(d_error.data)

            # Perform the update
            optimizer.step()
            num_param_updates += 1
            print("num param_updates ==> ", num_param_updates)

            # Periodically update the target network by Q network to target Q network
            if num_param_updates % target_update_freq == 0:
                target_Q.load_state_dict(Q.state_dict())
                target_Q.save(Q, './data/')
