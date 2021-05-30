### Exercises -> width - kernel_size + 1
import torch
import torchvision
from torchvision import transforms
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

class NN_Model_K(nn.Module):
    def __init__(self, n_channel):
        super().__init__()
        self.n_channel = n_channel
        self.conv1 = nn.Conv2d(3, n_channel, kernel_size=(1,3), padding=(0,1))
        self.bn1 = nn.BatchNorm2d(num_features=n_channel)
        self.conv2 = nn.Conv2d(n_channel, n_channel//2, kernel_size=(1,3), padding=(0,1))
        self.bn2 = nn.BatchNorm2d(num_features=n_channel//2)
        self.fc1 = nn.Linear(8 * 8 * n_channel//2 , 32)
        self.fc2 = nn.Linear(32, 2)
        
    def forward(self, x):
        out = self.bn1(self.conv1(x))
        out = F.max_pool2d(torch.relu(out), 2)
        out = self.bn2(self.conv2(out))
        out = F.max_pool2d(torch.relu(out), 2)
        out = out.view(-1, 8 * 8 * self.n_channel // 2)
        out = torch.relu(self.fc1(out))
        out = self.fc2(out)
        return out
