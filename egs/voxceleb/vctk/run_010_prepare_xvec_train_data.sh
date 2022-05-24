#!/bin/bash
# Copyright
#                2020   Johns Hopkins University (Author: Jesus Villalba)
# Apache 2.0.
#
. ./cmd.sh
. ./path.sh
set -e

stage=1
config_file=default_config.sh

. parse_options.sh || exit 1;
. $config_file

# DAMI - TODO: should this be updated in the script below?
# --storage_name vctk-$(date +'%m_%d_%H_%M') --use-bin-vad true \
# This is required for training and validation
# for .. loop on train and validation

# ./run_010_prepare_xvec_train_data.sh --stage 1
if [ $stage -le 1 ]; then
    # This script preprocess audio for x-vector training
    # steps_xvec/preprocess_audios_for_nnet_train.sh --nj 40 --cmd "$train_cmd" \
	# --storage_name voxceleb-v1.1-$(date +'%m_%d_%H_%M') --use-bin-vad true \
	# data/${nnet_data} data/${nnet_data}_proc_audio_no_sil exp/${nnet_data}_proc_audio_no_sil
    # hyp_utils/kaldi/utils/fix_data_dir.sh data/${nnet_data}_proc_audio_no_sil

    # steps_xvec/preprocess_audios_for_nnet_train.sh --nj 40 --cmd "$train_cmd" \
    # --storage_name vctk-$(date +'%m_%d_%H_%M') --use-bin-vad true \
	# data/${nnet_data} data/${nnet_data}_proc_audio_no_sil exp/${nnet_data}_proc_audio_no_sil
    # hyp_utils/kaldi/utils/fix_data_dir.sh data/${nnet_data}_proc_audio_no_sil

    # TODO: for .. loop on train and validation 
    steps_xvec/preprocess_audios_for_nnet_train.sh --nj 40 --cmd "$train_cmd" \
    --storage_name vctk-$(date +'%m_%d_%H_%M') --use-bin-vad true \
	data/${nnet_data_train} data/${nnet_data_train}_proc_audio_no_sil exp/${nnet_data_train}_proc_audio_no_sil
    hyp_utils/kaldi/utils/fix_data_dir.sh data/${nnet_data_train}_proc_audio_no_sil

    #  steps_xvec/preprocess_audios_for_nnet_train.sh --nj 40 --cmd "$train_cmd" \
    # --storage_name vctk-$(date +'%m_%d_%H_%M') --use-bin-vad true \
	# data/${nnet_data_validation} data/${nnet_data_validation}_proc_audio_no_sil exp/${nnet_data_validation}_proc_audio_no_sil
    # hyp_utils/kaldi/utils/fix_data_dir.sh data/${nnet_data_validation}_proc_audio_no_sil

fi

# ./run_010_prepare_xvec_train_data.sh --stage 2
if [ $stage -le 2 ]; then
    # This script preprocess audio for x-vector training
    echo "SKIP 2..."
    # steps_xvec/preprocess_audios_for_nnet_train.sh --nj 40 --cmd "$train_cmd" \
    # --storage_name vctk-$(date +'%m_%d_%H_%M') --use-bin-vad true \
	# data/${nnet_data_validation} data/${nnet_data_validation}_proc_audio_no_sil exp/${nnet_data_validation}_proc_audio_no_sil
    # hyp_utils/kaldi/utils/fix_data_dir.sh data/${nnet_data_validation}_proc_audio_no_sil

fi

# ./run_010_prepare_xvec_train_data.sh --stage 3, 5

# ./run_010_prepare_xvec_train_data.sh --stage 3
if [ $stage -le 3 ]; then
    # This script preprocess audio for x-vector training
    # echo "SKIP 3..."
    steps_xvec/preprocess_audios_for_nnet_train.sh --nj 40 --cmd "$train_cmd" \
    --storage_name vctk-$(date +'%m_%d_%H_%M') --use-bin-vad true \
	data/${nnet_data_test} data/${nnet_data_test}_proc_audio_no_sil exp/${nnet_data_test}_proc_audio_no_sil
    hyp_utils/kaldi/utils/fix_data_dir.sh data/${nnet_data_test}_proc_audio_no_sil

fi


# # ./run_010_prepare_xvec_train_data.sh --stage 4
# DAMI - TODO: see hyp_utils directory
# this is specfic to speaker id. 
# don't need this for accent.

# this may not be required, leave it for now
if [ $stage -le 4 ]; then
    echo "SKIP 4..."
    # Now, we remove files with less than 4s
    # hyp_utils/remove_short_audios.sh --min-len 4 data/${nnet_data}_proc_audio_no_sil

    # We also want several utterances per speaker. Now we'll throw out speakers
    # with fewer than 4 utterances.
    # hyp_utils/remove_spk_few_utts.sh --min-num-utts 4 data/${nnet_data}_proc_audio_no_sil

fi


# ./run_010_prepare_xvec_train_data.sh --stage 5
# DAMI - TODO: go back to run_001 and make_vctk
#              and change to flow into this pipeline
#              the train and validation split is being 
#              done here 
# this is required. 
if [ $stage -le 5 ]; then

    echo "5... make_vctk_v02"
    # Prepare train and validation lists for x-vectors
    # local/make_train_lists_sup_embed_with_augm.sh \       # DAMI - TODO: utterance to accent
	# data/${nnet_data_train}_proc_audio_no_sil \           # input directory
	# data/${nnet_data_train}_proc_audio_no_sil/lists_xvec  # output directory

    # DAMI - TODO: remove this and add my script here
    # local/make_vctk_v02.py $vctk_root dev 16 data/0/train
    local/make_vctk_v02.py $vctk_root dev 16 data/0/test
fi

exit
