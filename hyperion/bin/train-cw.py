#!/usr/bin/env python

"""
Trains Centering and whitening
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

from hyperion.io import HypDataReader
from hyperion.helpers import VectorReader as VR
from hyperion.pdfs.core import Normal
from hyperion.transforms import TransformList, CentWhiten, LNorm
from hyperion.utils.scp_list import SCPList



def load_model(input_path, with_lnorm, name, **kwargs):

    if input_path is None:
        if with_lnorm:
            return LNorm(name=name, **kwargs)
        else:
            return CentWhiten(name=name, **kwargs)

    try:
        if with_lnorm:
            return LNorm.load(input_path)
        else:
            return CentWhiten(input_path)
    except:
        tfl = TransformList.load(input_path)
        for tf in tfl.transforms:
            if tf.name == name:
                return tf
            


def train_cw(iv_file, train_list, preproc_file, with_lnorm,
             save_tlist, append_tlist, input_path, output_path, **kwargs):
    
    if preproc_file is not None:
        preproc = TransformList.load(preproc_file)
    else:
        preproc = None

    vr_args = VR.filter_args(**kwargs)
    vr = VR(iv_file, train_list, preproc, **vr_args)
    x = vr.read()

    t1 = time.time()

    model_args = CentWhiten.filter_args(**kwargs)
    model = load_model(input_path, with_lnorm, **model_args)
    
    model.fit(x)

    print('Elapsed time: %.2f s.' % (time.time()-t1))
    
    x = model.predict(x)

    gauss=Normal(x_dim=x.shape[1])
    gauss.fit(x=x)
    print(gauss.mu[:4])
    print(gauss.Sigma[:4,:4])

    if save_tlist:
        if append_tlist and preproc is not None:
            preproc.append(model)
            model = preproc
        else:
            model = TransformList(model)

    model.save(output_path)
        
    
    
if __name__ == "__main__":

    parser=argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        fromfile_prefix_chars='@',
        description='Train Centering+Whitening')

    parser.add_argument('--iv-file', dest='iv_file', required=True)
    parser.add_argument('--train-list', dest='train_list', required=True)
    parser.add_argument('--preproc-file', dest='preproc_file', default=None)
    
    VR.add_argparse_args(parser)
    CentWhiten.add_argparse_args(parser)
    
    parser.add_argument('--input-path', dest='input_path', default=None)
    parser.add_argument('--output-path', dest='output_path', required=True)
    parser.add_argument('--no-lnorm', dest='with_lnorm',
                        default=True, action='store_false')

    parser.add_argument('--no-save-tlist', dest='save_tlist',
                        default=True, action='store_false')
    parser.add_argument('--no-append-tlist', dest='append_tlist', 
                        default=True, action='store_false')

    args=parser.parse_args()
    
    train_cw(**vars(args))

            
