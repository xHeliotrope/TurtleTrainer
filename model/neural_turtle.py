import torch as T
import torch.nn as nn
import torch.nn.functional as F
from torch import optim
import numpy as np

class DeepQTurtle(nn.Module):
    """inspired by https://www.youtube.com/watch?v=1XX6N-Gq7Tc
    """
    def __init__(self, in_channels=4, num_actions=18):
        super(DeepQTurtle, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, 32, 8, stride=4, padding=1)
        self.conv2 = nn.Conv2d(32, 64, 4, stride=2)
        self.conv3 = nn.Conv2d(64, 128, 3)
        self.fc1 = nn.Linear(128*19*8, 512)
        self.fc2 = nn.Linear(512, num_actions)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = F.relu(self.fc1(x.view(x.size(0), -1)))
        return self.fc2(x)
