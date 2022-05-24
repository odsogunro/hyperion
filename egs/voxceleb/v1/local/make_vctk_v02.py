#!/usr/bin/env python3
# chmod +x make_vctk_v02.py
# date: 2022 spring - 20220518
# author: olorundamilola 'dami' kazeem

# imports
# from ast import Break
import glob as gl
import pathlib as pl

import pandas as pd
import sklearn.model_selection as skms
import numpy as np

def get_train_validation_split(
    input_dir="/data/0/train_proc_audio_no_sil/",
    classify_by_file='utt2accent',
    output_dir="/data/0/train_proc_audio_no_sil/lists_xvec/",
    file_name='train.scp',
    num_splits=1,
    validation_percent=0.2, 
    stratify_using='ACCENT'
    ):
    '''
        input --> /data/0/train_proc_audio_no_sil/utt2accent:
            utt2accent file
                225-p225_002 English
                225-p225_003 English
                ...
                364-p364_278 Irish
                364-p364_302 Irish

        output --> /data/0/train_proc_audio_no_sil/lists_xvec/:
            class2int
            dev.scp
            test.scp
            train.scp
    '''

    input_dir_data = pl.Path(input_dir + classify_by_file)
    df_data = pd.read_csv(input_dir_data, header=None, delimiter=' ')
    df_data.columns = ['UTTERANCE', 'ACCENT']
    # df_data.columns = ['SPKID', 'UTTERANCE', 'ACCENT']
    
    output_dir = pl.Path(output_dir)
    print(output_dir, output_dir.parent)
    output_dir.mkdir(parents=True, exist_ok=True)

    # variables
    X = df_data
    y = X[stratify_using]
    # y = X[['SPKID', 'ACCENT']]


    #####
    # class2int
    #####
    labels = list(set(y))
    print("ACCENTS for class2int file: \n", labels)
    
    class_2_int = 'class2int'
    class_2_int = pl.Path(output_dir / class_2_int)
    for label in labels:
        # print(class_2_int, label)
        class_2_int.open('a').write(label + '\n')

    print("DONE writing - class2int file")


    #####
    # train.scp
    # val.scp
    #####

    # random seed
    einsof = 42

    # if (validation_percent == 0.0):
    #     # test and no validation
    #     pass
    
    # else:
    #     # train and validation
    #     pass 

    skf = skms.StratifiedShuffleSplit(n_splits=num_splits, test_size=validation_percent, random_state=einsof)
    skf = skf.split(X, y)

    # print(dir_data, "\n", df_data, "\n", skf)

    for i, (train_index, test_index) in enumerate(skf):
        X_train = X.iloc[list(train_index), :]
        y_train = X_train[stratify_using]
        X_validation = X.iloc[list(test_index), :]
        y_validation = X_validation[stratify_using]

        # print("COUNT", i, "HERE NOW - TRAIN: \n", X_train, y_train)
        # print()
        # print("COUNT", i, "HERE NOW - VALIDATION: \n", X_validation, y_validation)
        # print()
        # print(type(X_train["UTTERANCE"]), " ", type(X_train["ACCENT"]))
        # print(list(X_train["UTTERANCE"]), " ", list(X_train["ACCENT"]))
        
        train_scp = file_name # 'train.scp' or test.scp
        train_scp = pl.Path(output_dir / train_scp)

        train_utterance = list(X_train["UTTERANCE"])
        train_accent = list(X_train["ACCENT"])
        train_length = len(train_utterance)
        for tl in range(train_length):
            print(train_utterance[tl], " ", train_accent[tl])
            train_scp.open('a').write(train_utterance[tl] + " " + train_accent[tl] + '\n')

        validation_scp = 'val.scp'
        validation_scp = pl.Path(output_dir / validation_scp)

        validation_utterance = list(X_validation["UTTERANCE"])
        validation_accent = list(X_validation["ACCENT"])
        validation_length = len(validation_utterance)
        for vl in range(validation_length):
            print(validation_utterance[vl], validation_accent[vl])
            validation_scp.open('a').write(validation_utterance[vl] + " " + validation_accent[vl] + '\n')
        
        break # DAMI - TODO: release later to get more folds


def main():

    ###
    # create train and validation
    ###
    # train_and_validation = get_train_validation_split(
    #     input_dir="./data/0/train_proc_audio_no_sil/",
    #     classify_by_file='utt2accent',
    #     output_dir="./data/0/train_proc_audio_no_sil/lists_xvec/",
    #     file_name="train.scp",
    #     num_splits=1,
    #     validation_percent=0.2, 
    #     stratify_using='ACCENT'
    # )

    ###
    # create test and no validation
    ###
    test_and_no_validation = get_train_validation_split (
        # input_dir="./data/0/test/",
        input_dir="./data/0/test_proc_audio_no_sil/",
        classify_by_file='utt2accent',
        # output_dir="./data/0/test/lists_xvec/",
        output_dir="./data/0/test_proc_audio_no_sil/lists_xvec/",
        file_name="test.scp",
        num_splits=1,
        # validation_percent=0.0, 
        validation_percent=6,
        stratify_using='ACCENT'
    )

if __name__ == '__main__':
    main()

# run the script on the grid.
# python -m make_vctk_v02.py OR make_vctk_v02
