#!/bin/bash
# Copyright
#                2019   Johns Hopkins University (Author: Jesus Villalba)
# Apache 2.0.
#

# DAMI: first pass on accent classification script
# - SEE for example, /export/c01/dkazeem/hyperion/egs/voxceleb/adv.v2/run_022_attack_type_classif_allknown.sh

. ./cmd.sh
. ./path.sh
set -e

stage=1
ngpu=1

config_file=default_config.sh

resume=false
interactive=false
num_workers=4
xvec_use_gpu=false
xvec_chunk_length=12800

. parse_options.sh || exit 1;
. $config_file
. datapath.sh

if [ "$xvec_use_gpu" == "true" ];then
    xvec_args="--use-gpu true --chunk-length $xvec_chunk_length"
    xvec_cmd="$cuda_eval_cmd"
else
    xvec_cmd="$train_cmd"
fi

###
# ------ REMOVED
###
# batch_size=$(($sign_nnet_batch_size_1gpu*$ngpu))
# grad_acc_steps=$(echo $batch_size $sign_nnet_eff_batch_size | awk '{ print int($2/$1+0.5)}')
# log_interval=$(echo 100*$grad_acc_steps | bc)

# list_dir=data/$attack_type_split_tag
# list_dir="/data/0/train_proc_audio_no_sil/lists_xvec/class2int"

# args=""
# if [ "$resume" == "true" ];then
#     args="--resume"
# fi

# if [ "$interactive" == "true" ];then
#     export cuda_cmd=run.pl
# fi


#####
#
#####
# sign_nnet_reldir=$spknet_name/$sign_nnet_name/$attack_type_split_tag
# sign_nnet_dir=exp/sign_nnets/$sign_nnet_reldir
# sign_dir=exp/signatures/$sign_nnet_reldir
# logits_dir=exp/logits/$sign_nnet_reldir
# logits_dir=exp/logits/$...
# sign_nnet=$sign_nnet_dir/model_ep0020.pth

# # Network Training
# if [ $stage -le 1 ]; then
#     echo "Train signature network on all attacks"
#     mkdir -p $sign_nnet_dir/log
#     $cuda_cmd --gpu $ngpu $sign_nnet_dir/log/train.log \
# 	hyp_utils/conda_env.sh --conda-env $HYP_ENV --num-gpus $ngpu \
# 	torch-train-xvec-from-wav.py  $sign_nnet_command --cfg $sign_nnet_config \
# 	--audio-path $list_dir/trainval_wav.scp \
# 	--time-durs-file $list_dir/trainval_utt2dur \
# 	--train-list $list_dir/train_utt2attack \
# 	--val-list $list_dir/val_utt2attack \
# 	--class-file $list_dir/class_file \
# 	--batch-size $batch_size \
# 	--num-workers $num_workers \
# 	--grad-acc-steps $grad_acc_steps \
# 	--num-gpus $ngpu \
# 	--log-interval $log_interval \
# 	--exp-path $sign_nnet_dir $args
# fi

# if [ $stage -le 2 ]; then
#     echo "Extract signatures on the test set"
#     mkdir -p $list_dir/test
#     cp $list_dir/test_wav.scp $list_dir/test/wav.scp
#     nj=100
#     steps_xvec/extract_xvectors_from_wav.sh \
# 	--cmd "$xvec_cmd --mem 6G" --nj $nj ${xvec_args} --use-bin-vad false \
# 	--feat-config $feat_config \
# 	$sign_nnet $list_dir/test \
# 	$sign_dir/test
# fi
###
# ------ REMOVED
###

# DAMI - TODO: modify stage/step 3, 4, and 5 --> 1, 2 ,3 


# sign_dir_dami=exp/xvectors/fbank80_stmn_lresnet34_e256_arcs30m0.3_do0_adam_lr0.05_b512.v1
# # proj_dir=$sign_dir/voxceleb1_test/tsne
# # proj_dir=$sign_dir/vctk_test/tsne
# proj_dir=exp/vctk_test/tsne
# # if [ $stage -le 3 ];then
# if [ $stage -le 1 ];then
#     echo "Make TSNE plots on all accents"
#     echo "Result will be left in $proj_dir"
#     for p in 30 100 250
#     do
# 	for e in 12 64
# 	do
# 	    proj_dir_i=$proj_dir/p${p}_e${e}
# 	    $train_cmd $proj_dir_i/train.log \
# 		steps_visual/proj-attack-tsne.py \
# 		# --train-v-file scp:$sign_dir/voxceleb1_test/xvector.scp \
#         # --train-v-file scp:$sign_dir/vctk_test/xvector.scp \
#         --train-v-file scp:$sign_dir_dami/0/test/xvector.scp
# 		# --train-list $list_dir/utt2attack \
#         --train-list $list_dir/utt2accent \
#         --train-list egs/voxceleb/vctk/data/0/test/utt2accent
# 		--pca-var-r 0.99 \
# 		--prob-plot 0.3 --lnorm \
# 		--tsne.metric cosine --tsne.early-exaggeration $e --tsne.perplexity $p --tsne.init pca \
# 		--output-path $proj_dir_i &
# 	done
#     done
#     wait
# fi


# DAMI - TODO: find the $logits_dir
logits_dir=exp/logits
sign_nnet=exp/xvector_nnets/fbank80_stmn_lresnet34_e256_arcs30m0.3_do0_adam_lr0.05_b512.v1/model_ep0030.pth
# list_dir=data/0/train_proc_audio_no_sil
list_dir=data/0/test_proc_audio_no_sil
# class_loc=data/0/train_proc_audio_no_sil/lists_xvec
class_loc=data/0/test_proc_audio_no_sil/lists_xvec
# if [ $stage -le 4 ];then
if [ $stage -le 2 ]; then
    # echo "Eval signature network logits on test attacks"
    echo "Eval signature accent logits on test accents"
    nj=100
    steps_xvec/eval_xvec_logits_from_wav.sh \
	--cmd "$xvec_cmd --mem 6G" --nj $nj ${xvec_args} --use-bin-vad false \
	--feat-config $feat_config \
	$sign_nnet $list_dir \
    $logits_dir/vctk_test
    # steps_xvec/eval_xvec_logits_from_wav.sh \
	# --cmd "$xvec_cmd --mem 6G" --nj $nj ${xvec_args} --use-bin-vad false \
	# --feat-config $feat_config \
	# $sign_nnet $list_dir \
	# $logits_dir/voxceleb1_test
fi

# if [ $stage -le 5 ];then
score_file=${logits_dir}/vctk_test/logits.scp
key_file=${list_dir}/lists_xvec/test.scp
class_file=${class_loc}/class2int

if [ $stage -le 3 ];then

    echo "Compute cofusion matrices"
    # echo "Result is left in $logits_dir/voxceleb1_test/eval_acc.log"
    echo "Result is left in $logits_dir/vctk_test/eval_acc.log"
    echo "SCORE FILE: $score_file"
    echo "KEY FILE: $key_file"
    echo "CLASS FILE: $class_file"
    $train_cmd $logits_dir/vctk_test/eval_acc.log \
        hyp_utils/conda_env.sh steps_backend/eval-classif-perf.py \
        --score-file scp:$score_file \
        --key-file $key_file \
	    --class-file $class_file
fi

# if [ $stage -le 3 ];then
#     echo "Compute cofusion matrices"
#     # echo "Result is left in $logits_dir/voxceleb1_test/eval_acc.log"
#     echo "Result is left in $logits_dir/vctk_test/eval_acc.log"
#     # $train_cmd $logits_dir/voxceleb1_test/eval_acc.log \
#     $train_cmd $logits_dir/vctk_test/eval_acc.log \
#         hyp_utils/conda_env.sh steps_backend/eval-classif-perf.py \
#         # steps_backend/eval-classif-perf.py \
#         # --score-file scp:$logits_dir/voxceleb1_test/logits.scp \
#         # --key-file $list_dir/utt2attack \
#         # egs/voxceleb/vctk/exp/logits/vctk_test/logits.scp
#         --score-file scp:$logits_dir/vctk_test/logits.scp \
#         --key-file ${key_file} \
# 	    --class-file $class_loc/class2int
# fi

exit
