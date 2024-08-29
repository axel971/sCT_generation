import pathlib as Path
import numpy as np
from torch import nn
import torch

def conv_block(in_channels: int,
               out_channels: int,
               kernel_size: tuple):
    
    x = nn.Sequential(

            nn.Conv2d(in_channels = in_channels,
                      out_channels = out_channels,
                      kernel_size = kernel_size,
                      stride = 1,
                      padding = "same"
                      ),

            nn.BatchNorm2d(out_channels),
            nn.Mish(),
            nn.Conv2d(in_channels = out_channels,
                      out_channels = out_channels,
                      kernel_size = kernel_size,
                      stride = 1,
                      padding = "same"),
            nn.BatchNorm2d(out_channels),
            nn.Mish()
            )
    return x

def final_layers(in_channels: int,
                out_channels: int,
                kernel_size: tuple):

    return nn.Conv2d(in_channels = in_channels,
                     out_channels = out_channels,
                     kernel_size = kernel_size,
                     padding = 'same',
                     stride = 1)
    
def downsampling(in_channels: int,
                  out_channels: int):

    return nn.Conv2d(in_channels = in_channels,
                     out_channels = out_channels,
                     kernel_size = 2,
                     stride = 2,
                     padding = 0)

def upsampling(in_channels: int,
                out_channels: int):
    
    return nn.ConvTranspose2d(in_channels = in_channels,
                              out_channels = out_channels,
                              kernel_size = 2,
                              stride = 2,
                              padding = 0)

class UNet_2d(nn.Module):

    def __init__(self,
                 input_shape: int,
                 output_shape: int
                 ) -> None:

        super().__init__()
    
        self.conv_block_e1 = conv_block(input_shape, 64, (3,3))
        self.conv_block_e2 = conv_block(128, 128, (3, 3))
        self.conv_block_e3 = conv_block(256, 256, (3, 3))
       
        self.conv_block_b = conv_block(512, 512, (3, 3))

        self.conv_block_d1 = conv_block(64 * 2, 64, (3,3))
        self.conv_block_d2 = conv_block(128 * 2, 128, (3, 3))
        self.conv_block_d3 = conv_block(256 * 2, 256, (3, 3))
        
        self.downsampling_e1 = downsampling(64, 128)
        self.downsampling_e2 = downsampling(128, 256)
        self.downsampling_e3 = downsampling(256, 512)

        self.upsampling_d1  = upsampling(128, 64)
        self.upsampling_d2 = upsampling(256, 128)
        self.upsampling_d3 = upsampling(512, 256)
        
        self.final_layers = final_layers(64, output_shape, (3,3)) 

    def forward(self, x):
        
        # Encoding
        e1 = self.conv_block_e1(x)
        ds1 = self.downsampling_e1(e1)

        e2 = self.conv_block_e2(ds1)
        ds2 = self.downsampling_e2(e2)

        e3 = self.conv_block_e3(ds2)
        ds3 = self.downsampling_e3(e3)

        # Bottleneck
        b =  self.conv_block_b(ds3)

        # Decoding 
        us3 = self.upsampling_d3(b)
        d3 = self.conv_block_d3(torch.cat([us3, e3], axis = 1))

        us2 = self.upsampling_d2(d3)
        d2 = self.conv_block_d2(torch.cat([us2, e2], axis = 1))

        us1 = self.upsampling_d1(d2)
        d1 = self.conv_block_d1(torch.cat([us1, e1], axis = 1))
        
        # Final layers
        return self.final_layers(d1)
        

