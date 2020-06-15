"""
 Copyright 2020 Johns Hopkins University  (Author: Jesus Villalba)
 Apache 2.0  (http://www.apache.org/licenses/LICENSE-2.0)
"""
import torch.nn as nn
from torch.nn import Conv2d, BatchNorm2d, Dropout2d

from ..layers import ActivationFactory as AF
from ..layers.subpixel_convs import SubPixelConv2d

def _convkxk(in_channels, out_channels, kernel_size=3, stride=1, groups=1, dilation=1, bias=False):
    """kernel k convolution with padding"""
    padding = dilation*(kernel_size-1)//2
    return Conv2d(in_channels, out_channels, kernel_size=kernel_size, stride=stride,
                  padding=padding, groups=groups, bias=bias, dilation=dilation, 
                  padding_mode='reflection')


def _conv1x1(in_channels, out_channels, stride=1, bias=False):
    """point-wise convolution"""
    return Conv2d(in_channels, out_channels, kernel_size=1, stride=stride, bias=bias)


def _subpixel_conv1x1(in_channels, out_channels, stride=1, bias=False):
    """point-wise subpixel convolution"""
    return SubPixelConv2d(in_channels, out_channels, kernel_size=1, stride=stride, bias=bias)


def _subpixel_convkxk(in_channels, out_channels, kernel_size=3, stride=1, groups=1, dilation=1, bias=False):
    """kernel k subpixel convolution with padding"""
    padding = dilation*(kernel_size-1)//2
    return SubPixelConv2d(in_channels, out_channels, kernel_size=kernel_size, stride=stride,
                  padding=padding, groups=groups, bias=bias, dilation=dilation, 
                  padding_mode='reflection')


def _make_downsample(in_channels, out_channels, stride, norm_layer, norm_before):

    if norm_before:
        return nn.Sequential(
            _conv1x1(in_channels, out_channels, stride, bias=False), 
            norm_layer(out_channels))
    
    return _conv1x1(in_channels, out_channels, stride, bias=True) 


def _make_upsample(in_channels, out_channels, stride, norm_layer, norm_before):

    if norm_before:
        return nn.Sequential(
            _subpixel_conv1x1(in_channels, out_channels, stride, bias=False), 
            norm_layer(out_channels))
    
    return _subpixel_conv1x1(in_channels, out_channels, stride, bias=True) 


class ResNet2dBasicBlock(nn.Module):
    expansion = 1

    #__constants__ = ['downsample']

    def __init__(self, in_channels, channels, kernel_size=3,
                 activation='relu6',
                 stride=1, dropout_rate=0, groups=1, dilation=1, 
                 use_norm=True, norm_layer=None, norm_before=True):

        super().__init__()

        self.norm_before = False
        self.norm_after = False
        if use_norm:
            if norm_layer is None:
                norm_layer = BatchNorm2d
            self.bn1 = norm_layer(channels)            
            self.bn2 = norm_layer(channels)
            if norm_before:
                self.norm_before = True
            else:
                self.norm_after = True

        self.in_channels = in_channels
        self.channels = channels

        bias = not norm_before
        self.conv1 = _convkxk(in_channels, channels, kernel_size, stride, groups, dilation, bias=bias)
        self.act1 = AF.create(activation)
        self.conv2 = _convkxk(channels, channels, kernel_size, groups=groups, bias=bias)

        self.act2 = AF.create(activation)
        self.stride = stride

        self.downsample = None
        if stride != 1 or in_channels != channels:
            self.downsample = _make_downsample(in_channels, channels, 
                                               stride, norm_layer, norm_before)
        self.dropout_rate = dropout_rate
        self.dropout = None
        if dropout_rate > 0:
            self.dropout = Dropout2d(dropout_rate)

        self.context = (stride + dilation)*(kernel_size-1)//2
        self.downsample_factor = stride


    @property
    def out_channels(self):
        return self.channels


    def forward(self, x):
        residual = x

        x = self.conv1(x)
        if self.norm_before:
            x = self.bn1(x)

        x = self.act1(x)

        if self.norm_after:
            x = self.bn1(x)

        x = self.conv2(x)

        if self.norm_before:
            x = self.bn2(x)

        if self.downsample is not None:
            residual = self.downsample(residual)

        x += residual
        x = self.act2(x)

        if self.norm_after:
            x = self.bn2(x)
        
        if self.dropout_rate > 0:
            x = self.dropout(x)

        return x


class ResNet2dBasicDecBlock(nn.Module):
    expansion = 1

    #__constants__ = ['downsample']

    def __init__(self, in_channels, channels, kernel_size=3,
                 activation='relu6',
                 stride=1, dropout_rate=0, groups=1, dilation=1, 
                 use_norm=True, norm_layer=None, norm_before=True):

        super().__init__()

        self.norm_before = False
        self.norm_after = False
        if use_norm:
            if norm_layer is None:
                norm_layer = BatchNorm2d
            self.bn1 = norm_layer(channels)            
            self.bn2 = norm_layer(channels)
            if norm_before:
                self.norm_before = True
            else:
                self.norm_after = True

        self.in_channels = in_channels
        self.channels = channels

        bias = not norm_before
        self.conv1 = _subpixel_convkxk(in_channels, channels, kernel_size, stride, groups, dilation, bias=bias)

        self.act1 = AF.create(activation)
        self.conv2 = _convkxk(channels, channels, kernel_size, groups=groups, bias=bias)

        self.act2 = AF.create(activation)
        self.stride = stride

        self.upsample = None
        if stride != 1 or in_channels != channels:
            self.upsample = _make_upsample(in_channels, channels, 
                                           stride, norm_layer, norm_before)
        self.dropout_rate = dropout_rate
        self.dropout = None
        if dropout_rate > 0:
            self.dropout = Dropout2d(dropout_rate)

        self.context = (stride + dilation)*(kernel_size-1)//2
        self.upsample_factor = stride


    @property
    def out_channels(self):
        return self.channels


    def forward(self, x):
        residual = x

        x = self.conv1(x)
        if self.norm_before:
            x = self.bn1(x)

        x = self.act1(x)

        if self.norm_after:
            x = self.bn1(x)

        x = self.conv2(x)

        if self.norm_before:
            x = self.bn2(x)

        if self.upsample is not None:
            residual = self.upsample(residual)

        x += residual
        x = self.act2(x)

        if self.norm_after:
            x = self.bn2(x)
        
        if self.dropout_rate > 0:
            x = self.dropout(x)

        return x

