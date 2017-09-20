#!/usr/bin/env python

"""
Plot histogram of i-vectors
"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from six.moves import xrange

import sys
import os
import argparse
import time

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from hyperion.io import HypDataReader
from hyperion.helpers import VectorReader as VR
from hyperion.transforms import TransformList



def plot_vector_hist(iv_file, v_list, preproc_file, output_path, num_bins, normed, **kwargs):
    
    if preproc_file is not None:
        preproc = TransformList.load(preproc_file)
    else:
        preproc = None

    vr_args = VR.filter_args(**kwargs)
    vr = VR(iv_file, v_list, preproc, **vr_args)
    x = vr.read()

    t1 = time.time()

    if not os.path.exists(output_path):
        os.makedirs(ouput_path)

    for i in xrange(x.shape[1]):
        
        fig_file = '%s/D%04d.pdf' % (output_path, i)
        
        plt.hist(x[:,i], num_bins, normed=normed)
        plt.xlabel('Dim %d' % i)
        plt.grid(True)
        plt.show()
        plt.savefig(fig_file)
        plt.clf()
        

    print('Elapsed time: %.2f s.' % (time.time()-t1))

        
    
    
if __name__ == "__main__":

    parser=argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        fromfile_prefix_chars='@',
        description='Plots historgrams of i-vectors')

    parser.add_argument('--iv-file', dest='iv_file', required=True)
    parser.add_argument('--v-list', dest='v_list', required=True)
    parser.add_argument('--preproc-file', dest='preproc_file', default=None)
    
    VR.add_argparse_args(parser)
    
    parser.add_argument('--output-path', dest='output_path', required=True)
    parser.add_argument('--no-normed', dest='normed', default=True,
                        action='store_false')
    parser.add_argument('--num-bins', dest='num_bins', type=int, default=100)
                    
    args=parser.parse_args()
    
    plot_vector_hist(**vars(args))

            
