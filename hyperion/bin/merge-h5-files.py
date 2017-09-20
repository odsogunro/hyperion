#!/usr/bin/env python
"""
Merges multiple hdf5 files into one file
"""
from __future__ import absolute_import
from __future__ import print_function

import sys
import os
import argparse
import time
import numpy as np
from six.moves import xrange

from hyperion.io import H5Merger

def merge(input_files, output_path, chunk_size):

    m = H5Merger(input_files, output_path, chunk_size)
    m.merge()
    

if __name__ == "__main__":
    
    parser=argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        fromfile_prefix_chars='@',
        description='Merges multiple hdf5 files into one file')

    parser.add_argument('--input-files', dest='input_files', nargs='+', required=True)
    parser.add_argument('--output-path', dest='output_path', required=True)
    #parser.add_argument('--field', dest='field', default='')
    parser.add_argument('--chunk-size', dest='chunk_size', type=int, default=None)
    #parser.add_argument('--squeeze', dest='squeeze', default=False, action='store_true')

    args=parser.parse_args()

    merge(**vars(args))
    
