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

train=0/train 
validation=0/validation
test=0/test

# nnet_data=voxceleb2cat_train
# nnet_data=0/train
nnet_data=$train
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
nnet_num_epochs=1 # 70
nnet_dir=exp/xvector_nnets/$nnet_name
# nnet=$nnet_dir/model_ep0070.pth
nnet=$nnet_dir/model_ep0001.pth


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

