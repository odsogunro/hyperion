# VAE with symmetric DC1 encoder-decoder with 4 layers, 256 dim per layer, latent_dim=80, compression factor=8

nnet_data=voxceleb2cat_train
batch_size_1gpu=512
eff_batch_size=512 # effective batch size
min_chunk=400
max_chunk=400
ipe=1
lr=0.01
dropout=0
latent_dim=80
model_type=vae
narch=dc1d
vae_opt="--in-feats 80"
enc_opt="--enc.in-conv-channels 256 --enc.in-kernel-size 5 --enc.in-stride 1 --enc.conv-repeats 1 1 1 1 --enc.conv-channels 256 --enc.conv-kernel-sizes 3 --enc.conv-strides 1 2 2 2"
dec_opt="--dec.in-channels 80 --dec.in-conv-channels 256 --dec.in-kernel-size 3 --dec.in-stride 1 --dec.conv-repeats 1 1 1 1 --dec.conv-channels 256 --dec.conv-kernel-sizes 3 --dec.conv-strides 1 2 2 2"

opt_opt="--optim.opt-type adam --optim.lr $lr --optim.beta1 0.9 --optim.beta2 0.95 --optim.weight-decay 1e-5 --optim.amsgrad"
lrs_opt="--lrsched.lrsch-type exp_lr --lrsched.decay-rate 0.5 --lrsched.decay-steps 16000 --lrsched.hold-steps 16000 --lrsched.min-lr 1e-5 --lrsched.warmup-steps 8000 --lrsched.update-lr-on-opt-step"
nnet_name=${model_type}_${narch}_b4d256_z${latent_dim}_c8_do${dropout}_optv1_adam_lr${lr}_b${eff_batch_size}.$nnet_data
nnet_num_epochs=540
num_augs=5
nnet_dir=exp/vae_nnets/$nnet_name
nnet=$nnet_dir/model_ep0540.pth

# xvector network trained with recipe v1.1
xvec_nnet_name=fbank80_stmn_lresnet34_e256_arcs30m0.3_do0_adam_lr0.05_b512_amp.v1
xvec_nnet_dir=../v1.1/exp/xvector_nnets/$xvec_nnet_name
xvec_nnet=$xvec_nnet_dir/model_ep0070.pth
