# Default parameters
# LResNet34 x-vector without mixed precision training

# acoustic features
feat_config=conf/fbank80_stmn_16k.yaml
feat_type=fbank80_stmn

#vad
vad_config=conf/vad_16k.yaml

# x-vector training 
# DAMI - ...
# DAMI - TODO: need to update this to data/#/train with a loop 
  	# to go through #'s from 0 to n-1 kfolds. first, this test run.
    # TODO: for .. loop through this
train=0/train 
validation=0/validation
test=0/test

# nnet_data=voxceleb2cat_train
# nnet_data=0/train
nnet_data=${train}

nnet_data_train=${train}
nnet_data_validation=${validation}
nnet_data_test=${test}

nnet_num_augs=6
aug_opt="--train-aug-cfg conf/reverb_noise_aug.yaml --val-aug-cfg conf/reverb_noise_aug.yaml"

batch_size_1gpu=64 # batch size default is 128. DAMI-TODO: changed to 64
eff_batch_size=512 # effective batch size default is 512. Should I change the reduce effective batch size?
ipe=$nnet_num_augs
min_chunk=4
max_chunk=4
lr=0.05 # DAMI - TODO: learning rate 

nnet_type=lresnet34 #light resnet
dropout=0
embed_dim=256

s=30
margin_warmup=20
margin=0.3

# DAMI - TODO: figure out these hyperparameters
nnet_opt="--resnet-type $nnet_type --in-feats 80 --in-channels 1 --in-kernel-size 3 --in-stride 1 --no-maxpool"
# DAMI - TODO: figure out these hyperparameters - see, pytorch adam optimizer, https://pytorch.org/docs/stable/generated/torch.optim.Adam.html
opt_opt="--optim.opt-type adam --optim.lr $lr --optim.beta1 0.9 --optim.beta2 0.95 --optim.weight-decay 1e-5 --optim.amsgrad"
# DAMI - TODO: figure out these hyperparameters  - see, pytorch adam optimizer, https://pytorch.org/docs/stable/generated/torch.optim.Adam.html
lrs_opt="--lrsched.lrsch-type exp_lr --lrsched.decay-rate 0.5 --lrsched.decay-steps 8000 --lrsched.hold-steps 40000 --lrsched.min-lr 1e-5 --lrsched.warmup-steps 1000 --lrsched.update-lr-on-opt-step"

nnet_name=${feat_type}_${nnet_type}_e${embed_dim}_arcs${s}m${margin}_do${dropout}_adam_lr${lr}_b${eff_batch_size}.v1
# DAMI - TODO: set to 1 for now
nnet_num_epochs=30 #50 # 70
nnet_dir=exp/xvector_nnets/$nnet_name
# nnet=$nnet_dir/model_ep0001.pth
nnet=$nnet_dir/model_ep0030.pth
# nnet=$nnet_dir/model_ep0050.pth
# nnet=$nnet_dir/model_ep0070.pth

# DAMI - TODO: ...
# back-end
plda_aug_config=conf/reverb_noise_aug.yaml
plda_num_augs=6
if [ $plda_num_augs -eq 0 ]; then
    # plda_data=voxceleb2cat_train
    plda_data=$train
else
    plda_data=voxceleb2cat_train_augx${plda_num_augs}
fi
plda_type=splda
lda_dim=200
plda_y_dim=150
plda_z_dim=200

# 5, 12, 19 failed


#####
# Quick and Dirty - Reuse of /egs/voxceleb/adv.v2/default_config.sh
#####

# Experiments using LResNet34 for x-vector extractor and for attack signature extractor
# We use only sucessful attacks
# We use attack SNR in (-100, 100) for train and test

# Victim model speaker LResNet34 x-vector configuration
spknet_command=resnet
# spknet_data=voxceleb2cat_train
spknet_data=${train}
# spknet_config=conf/lresnet34_spknet.yaml
# spknet_batch_size_1gpu=128
# spknet_eff_batch_size=512 # effective batch size
spknet_name=lresnet34
# spknet_dir=exp/xvector_nnets/$spknet_name
spknet_dir=${nnet_dir}
# spknet=$spknet_dir/model_ep0070.pth
spknet=${nnet}

# SpkID Attacks configuration
# feat_config=conf/fbank80_stmn_16k.yaml
# p_attack=0.25 #will try attacks in 25% of utterances
# attacks_common_opts="--save-failed --save-benign" #save failed attacks also

# SpkVerif Attacks configuration
p_tar_attack=0.1
p_non_attack=0.1
spkv_attacks_common_opts="--save-failed" #save failed attacks also


# Attack model LResNet34 configuration
# Accent model LResNet34 configuration
sign_nnet_command=resnet
sign_nnet_config=conf/lresnet34_atnet.yaml
sign_nnet_batch_size_1gpu=128
sign_nnet_eff_batch_size=512 # effective batch size
sign_nnet_name=lresnet34

# SNRs in -100, 100
# train_max_snr=100
# train_min_snr=-100
# test_max_snr=100
# test_min_snr=-100
# We only uses succesful attacks (attacks that changed the label)
# train_cat=success
# test_cat=success

# Splits options
# train and test on succesful attacks only, all SNR values
attack_type_split_opts="--train-success-category $train_cat --test-success-category $test_cat \
--train-max-snr $train_max_snr --train-min-snr $train_min_snr --test-max-snr $test_max_snr --test-min-snr $test_min_snr"
threat_model_split_opts="--train-success-category $train_cat --test-success-category $test_cat \
--train-max-snr $train_max_snr --train-min-snr $train_min_snr --test-max-snr $test_max_snr --test-min-snr $test_min_snr"
# for SNR we use same train/test SNR
snr_split_opts="--train-success-category $train_cat --test-success-category $test_cat \
--train-max-snr $test_max_snr --train-min-snr $test_min_snr --test-max-snr $test_max_snr --test-min-snr $test_min_snr"


# Experiment labels for experiments of attack classification with all attacks known
attack_type_split_tag="exp_attack_type_allknown"
snr_split_tag="exp_attack_snr_allknown"
threat_model_split_tag="exp_attack_threat_model_allknown"


# Known/Unknown attacks splits
known_attacks="fgsm iter-fgsm pgd-linf pgd-l1 pgd-l2"
unknown_attacks="cw-l2 cw-linf cw-l0"

# Experiment labels for datasets to train signatures with a subset of known attacks
sk_attack_type_split_tag="exp_attack_type_someknown"
sk_snr_split_tag="exp_attack_snr_someknown"
sk_threat_model_split_tag="exp_attack_threat_model_someknown"

# Experiment labels for attack verification with same attacks known and some unknown
attack_type_verif_split_tag="exp_attack_type_verif"
snr_verif_split_tag="exp_attack_snr_verif"
threat_model_verif_split_tag="exp_attack_threat_model_verif"

# Select attacks for attack verification, options are shared for the 3 tasks
# We use only successful attacks with all SNRs
verif_split_opts="--success-category $test_cat --max-snr $test_max_snr --min-snr $test_min_snr"

# Select attacks for attack novelty detection
# We use only successful attacks with all SNRs
novelty_split_opts="--success-category $test_cat --max-snr $test_max_snr --min-snr $test_min_snr"
novelty_split_tag="exp_attack_type_novelty"

# Experiment labels for experiments on attacks against speaker verification task
# Here we just do attack classification assuming all attacks known
spkverif_attack_type_split_tag="exp_spkverif_attack_type_allknown"
spkverif_snr_split_tag="exp_spkverif_attack_snr_allknown"
spkverif_threat_model_split_tag="exp_spkverif_attack_threat_model_allknown"
spkverif_split_opts="--test-success-category $test_cat --test-max-snr $test_max_snr --test-min-snr $test_min_snr"
