import torch
import torch.nn as nn
import numpy as np


class CNN_2d(nn.Module):
    
    def __init__(self):
        super().__init__()


        self.conv_block_1 = nn.Sequential(
                nn.Conv2d(in_channels = 1, out_channels = 64, kernel_size = 3, stride = 1, padding = "same"),
                nn.BatchNorm2d(num_features = 64),
                nn.Mish(),
                nn.Conv2d(in_channels = 64, out_channels = 64, kernel_size = 2, stride = 2)
                )

        self.conv_block_2 = nn.Sequential(
                nn.Conv2d(in_channels = 64, out_channels = 128, kernel_size = 3, stride = 1, padding = "same"),
                nn.BatchNorm2d(num_features = 128),
                nn.Mish(),
                nn.Conv2d(in_channels = 128, out_channels = 128, kernel_size = 2, stride = 2)
                )
        
        self.conv_block_3 = nn.Sequential(
                nn.Conv2d(in_channels = 128, out_channels = 256, kernel_size = 3, stride = 1, padding = "same"),
                nn.BatchNorm2d(num_features = 256),
                nn.Mish(),
                nn.Conv2d(in_channels = 256, out_channels = 256, kernel_size = 2, stride = 2)
                )

        self.mlp = nn.Sequential(
                nn.Flatten(),
                nn.LazyLinear(out_features = 256),
                nn.Mish(),
                nn.Linear(in_features = 256, out_features = 1),
                nn.Sigmoid()
                )

    def forward(self, x):

        return self.mlp(self.conv_block_3(self.conv_block_2(self.conv_block_1(x))))

class PrintLayer(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, x):
        
        print(x)

        return(x)
