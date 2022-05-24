#!/bin/bash
# Copyright
#                2018   Johns Hopkins University (Author: Jesus Villalba)
# Apache 2.0.
#
. ./cmd.sh
. ./path.sh
set -e

stage=1
config_file=default_config.sh

# DAMI - update parse_options.sh in utils/? No. 
. parse_options.sh || exit 1;
# DAMI - update datapath.sh in root of folder.
. datapath.sh 


if [ $stage -le 1 ];then
  # Prepare the VoxCeleb2 dataset for training.
  # local/make_voxceleb2cat.pl $voxceleb2_root dev 16 data/voxceleb2cat_train

  # Prepare the VCTK dataset for training.
  # DAMI - TODO: need to update this to data/#/train with a loop 
  # to go through #'s from 0 to n-1 kfolds. first, this test run.
  # DAMI - TODO: something along these lines is required.
  # - QUESTION: is this the most appropriate place for this?
  # local/make_vctk.py $vctk_root dev 16 
  # for i in {1..5}; do
  #   data/i/train
  # done

  # v0.0
  # local/make_vctk.py $vctk_root dev 16 data/0/train
  
  # v0.1
  local/make_vctk_v01.py $vctk_root dev 16 data/0/train


  # DAMI - TODO: UPDATE
  # for i in {1..5}; do
  #   echo ${i}
	# 	local/make_vctk.py $vctk_root dev 16 data/${i}/train
	# done
fi

# if [ $stage -le 2 ];then
  # prepare voxceleb1 for test
  # This script is for the old version of the dataset
  # local/make_voxceleb1_oeh.pl $voxceleb1_root data
  # Use this for the newer version of voxceleb1:
  
  # DAMI - removed this from running
  # local/make_voxceleb1_v2_oeh.pl $voxceleb1_root data
# fi
