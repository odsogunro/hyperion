"""
 Copyright 2019 Johns Hopkins University  (Author: Jesus Villalba)
 Apache 2.0  (http://www.apache.org/licenses/LICENSE-2.0)
"""
from __future__ import absolute_import

import numpy as np

import torch.nn as nn
from torch.nn import Conv1d, Linear, BatchNorm1d

from ..layers import ActivationFactory as AF
from ..layers import Dropout1d
from .etdnn_blocks import ETDNNBlock

class ResETDNNBlock(ETDNNBlock):

    def __init__(self, num_channels,
                 kernel_size, dilation=1, 
                 activation={'name':'relu', 'inplace': True},
                 dropout_rate=0,
                 use_batchnorm=True, batchnorm_before=False):

        super(ResETDNNBlock, self).__init__(num_channels, num_channels, 
                 kernel_size, dilation, activation, dropout_rate,
                 use_batchnorm, batchnorm_before)


    def forward(self, x):

        residual = x
        x = self.conv1(x)

        if self.batchnorm_before:
            x = self.bn1(x)

        x = self.activation1(x)
        
        if self.batchnorm_after:
            x = self.bn1(x)

        if self.dropout_rate > 0:
            x = self.dropout1(x)

        x = self.conv2(x)

        if self.batchnorm_before:
            x = self.bn2(x)

        x += residual
        x = self.activation2(x)
        
        if self.batchnorm_after:
            x = self.bn2(x)

        if self.dropout_rate > 0:
            x = self.dropout2(x)

        return x

