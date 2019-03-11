import torch as T
import torch.nn as nn
import torch.nn.functional as F
from torch import optim
import numpy as np

class DeepQTurtle(nn.Module):
    """inspired by https://www.youtube.com/watch?v=1XX6N-Gq7Tc
    """
    def __init__(self, num_actions=18):
        super(DeepQTurtle, self).__init__()
        self.conv1 = nn.Conv2d(4, 32, kernel_size=8, stride=4)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=4, stride=2)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=4, stride=1)
        self.fc4 = nn.Linear(128, 32)
        #self.fc4 = nn.Linear(128, 512)
        self.fc5 = nn.Linear(32, num_actions)

    def forward(self, x):
        print('hmmm')
        print(x.shape)
        print(x.size())
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        print(x.shape)
        print(x.size())
        x = F.relu(self.fc4(x.view(-1, x.size(1))))
        return self.fc5(x)
