import torch as T
import torch.nn as nn
import torch.nn.functional as F
from torch import optim
import numpy as np

class DeepQNet(nn.Module):
    """inspired by https://www.youtube.com/watch?v=1XX6N-Gq7Tc
    """
    def __init__(self, channels=4, num_actions=18):
        super(DeepQNet, self).__init__()
        self.conv1 = nn.Conv2d(channels, 32, kernel_size=8, stride=4)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=4, stride=2)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=4, stride=1)
        self.fc4 = nn.Linear(18400*4, 128)
        self.fc5 = nn.Linear(128, 32)
        self.fc6 = nn.Linear(32, num_actions)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = F.relu(self.fc4(x.view(32, 18400*4)))
        x = F.relu(self.fc5(x))
        x = F.relu(self.fc6(x))
        return x
