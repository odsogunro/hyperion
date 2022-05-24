#!/usr/bin/env python3
# chmod +x make_vctk_v01.py
# date: 2022 spring - 20220422
# author: olorundamilola 'dami' kazeem

# imports
import glob as gl
import pathlib as pl

import pandas as pd
import sklearn.model_selection as skms

# '/export/corpora5/VCTK-Corpus/wav48/p225/p225_001.wav'
def make_wav_scp(wave_files_list, spk_info_df, file_path="wav.scp"):
    """
        input:
            ...

        output:
            ...

        225-p225_001 /export/corpora5/VCTK-Corpus/wav48/p225/p225_001.wav
        id00012-21Uxsk56VDQ ffmpeg -v 8 -f concat -safe 0 -i data/voxceleb2cat_train/lists_cat/id00012-21Uxsk56VDQ.txt -f wav -acodec pcm_s16le -|

        file-name1 sox filepath1 -t wav -r 16000 - |

    `   http://sox.sourceforge.net/
        http://sox.sourceforge.net/sox.pdf

        https://pypi.org/project/sox/

        man sox
        sox --help
    """
    spks = set([i for i in spk_info_df["ID"]])
    print(spks)

    wav_scp_file = pl.Path(file_path)
    for wave in wave_files_list:
    
        wave = pl.Path(wave)
        spk = wave.parent.name[1:]
        
        if (int(spk) in spks):
            wav_scp_file.open("a").write(
                    str(wave.parent.name[1:]) 
                    + "-"
                    + str(wave.stem)
                    + " "
                    + "sox "
                    + str(wave)
                    + " -t wav -r 16000 -|"
                    + "\n"
                    )

# '/export/corpora5/VCTK-Corpus/wav48/p225'
def make_spk2utt(wav_files_dir, spk_info_df, file_path="spk2utt"):
    
    spks = set([i for i in spk_info_df["ID"]])
    print(spks)

    spk2utt_file = pl.Path(file_path)
    for wave_dir in wav_files_dir:
        
        spk = pl.Path(wave_dir).stem # p225
        spk = spk[1:] # 225

        if (int(spk) in spks):
            wave_file = sorted(pl.Path(wave_dir).glob("*.wav"))
            utt = ""
            for wave in wave_file:
                utt = utt + " " + str(spk) + "-" + str(wave.stem)
            spk2utt = spk + utt + "\n"
            spk2utt_file.open("a").write(spk2utt)

# make_spk2utt(test_dir, test_spkr_info)


def make_utt2spk(wav_files_dir, spk_info_df, file_path="utt2spk"):
    
    spks = set([i for i in spk_info_df["ID"]])
    print(spks)

    utt2spk_file = pl.Path(file_path)
    for wave_dir in wav_files_dir:
        spk = pl.Path(wave_dir).stem

        spk = spk[1:] # 225

        if (int(spk) in spks):
            wave_file = sorted(pl.Path(wave_dir).glob("*.wav"))
            utt = ""
            for wave in wave_file:
                utt = str(spk) + "-" + str(wave.stem)
                utt2spk = utt + " " + spk + "\n"
                utt2spk_file.open("a").write(utt2spk)

# make_utt2spk(test_dir, test_spkr_info)


def make_utt2accent(
    wav_files_dir, 
    spk_info_df, 
    file_path="utt2accent"):

    utt2accent_file = pl.Path(file_path)
    
    # # TODO - ASAP: need to convert speaker info to dataframe
    # # DONE - ... : convert spk_info txt to dataframe
    # spk_info = pd.read_csv(
    #     spk_info, delimiter="\s+", error_bad_lines=False, engine="python"
    # )   

    print("1. ", utt2accent_file)
    
    for wave_dir in wav_files_dir:
        spk = pl.Path(wave_dir).stem
        # print("2. ", spk)
        spk = spk[1:]
        # print("3. ", spk)

        # 248, 249, 250 - IndexError: index 0 is out of bounds for axis 0 with size 0
        # FAILS after 3. HERE below...

        # print("4. ", spk_info["ID"], spk_info["ID"] == int(spk))
        # accent = spk_info["ACCENTS"][spk_info["ID"] == int(spk)].values.item(0)

        try:
            print("4a. ", spk_info_df["ID"], spk_info_df["ID"] == int(spk))
            accent = spk_info_df["ACCENTS"][spk_info_df["ID"] == int(spk)].values.item(0)
            print("4b. ", accent)

            wave_file = sorted(pl.Path(wave_dir).glob("*.wav"))
            utt = ""
            
            for wave in wave_file:
                print("5. ", wave)
                utt = str(spk) + "-" + str(wave.stem)
                utt2accent = utt + " " + str(accent) + "\n"
                utt2accent_file.open("a").write(utt2accent)
                print("7. ", utt2accent)

        except:
            print("4c. not in dataframe!")

# make_utt2accent(test_dir, test_spkr_info, file_path="utt2accent") 
# make_utt2accent(test_dir, test_spkr_info, file_path="data/0/train/utt2accent")


def data_split_stratified(
    spk_dataframe,
    stratify_using="ACCENTS",
    train_percent=0.7,
    validation_percent=0.1,
    test_percent=0.2,
):
    X = spk_dataframe
    y = X[stratify_using]

    einsof = 42 # random seed

    # first stratified split of train and temp (i.e. dev/validation and test) sets
    X_train, X_val_and_test, y_train, y_val_and_test = skms.train_test_split(
        X, y, stratify=y, test_size=(1.0 - train_percent), random_state=einsof
    )

    # second stratified split to obtain validation and test sets
    X_validation, X_test, y_validation, y_test = skms.train_test_split(
        X_val_and_test,
        y_val_and_test,
        stratify=y_val_and_test,
        test_size=(test_percent / (validation_percent + test_percent)),
        random_state=einsof,
    )

    # return  X_train, X_dev_and_test, y_train, y_dev_and_test
    return X_train, X_validation, X_test

def data_split_stratified_kfold(
    spk_dataframe,
    wav_files,
    wav_dirs,
    stratify_using="ACCENTS",
    train_percent=0.7,
    validation_percent=0.1,
    test_percent=0.2,
    k_num_splits=2, # default = 5

):  

    kfold_dir_data = pl.Path("data")
    kfold_dir_data.mkdir(exist_ok=True)

    speaker_info = "speaker-info.txt"
    train = "train"
    validation = "validation"
    test = "test"

    # variables  
    X = spk_dataframe
    y = X[stratify_using]
   
    einsof = 42 # random seed

    # first stratified K fold shuffle split of train and temp (i.e. dev/validation and test) sets

    # skf = skms.StratifiedKFold(n_splits=k_num_splits, random_state=einsof, shuffle=True)
    # skf = skf.split(X, y)
    
    test_val_percent = validation_percent + test_percent
    skf = skms.StratifiedShuffleSplit(n_splits=k_num_splits, test_size=test_val_percent, random_state=einsof)
    skf = skf.split(X, y)

    for i, (train_index, val_and_test_index) in enumerate(skf):
        X_train = X.iloc[list(train_index), :]
        # y_train = y.iloc[list(train_index), :]
        X_val_and_test = X.iloc[list(val_and_test_index), :]
        # y_val_and_test = y.iloc[list(val_and_test_index), :]
        
        # y_train, y_test = y[train_index], y[val_and_test_index]
        # print(X_train, X_val_and_test, y_train, y_val_and_test)

        # second stratified split to obtain validation and test sets
        # NOPE! 
        #   - ValueError: The test_size = 3 should be greater or equal to the number of classes = 6
        X2 = X_val_and_test
        y2 = X2[stratify_using]
        # skf_vt = skms.StratifiedShuffleSplit(n_splits=1, test_size=validation_percent, random_state=einsof)
        # skf_vt = skf_vt.split(X2, y2)

        # for test_index, val_index in skf_vt:
        #     print("TEST \n", X.iloc[list(test_index), :])
        #     print("VAL \n", X.iloc[list(val_index), :])  

        # second stratified split to obtain validation and test sets
        X_validation, X_test, y_validation, y_test = skms.train_test_split(
            X2,
            y2,
            stratify=y2,
            test_size=(test_percent / (validation_percent + test_percent)),
            random_state=einsof,
        )

        print(type(X_train), " \n train >>> \n", X_train, "\n validation >>> \n", X_validation, "\n test >>> \n", X_test)
        # make directories
      
        # kfold_dir_data = pl.Path("data")
        # kfold_dir_data.mkdir(exist_ok=True)

        # speaker_info = "speaker-info.txt"
        # train = "train"
        # validation = "validation"
        # test = "test"

        #####
        # train
        #####
        kfold_dir_data = pl.Path("data")
        kfold_dir_data.mkdir(exist_ok=True)
        train = "train"
        speaker_info = "speaker-info.txt"
        kfold_dir_train = pl.Path(kfold_dir_data / str(i) / train) # /data/0/train
        # print(kfold_dir_train)
        kfold_dir_train.mkdir(parents=True, exist_ok=True)
        speaker_info = pl.Path(kfold_dir_train / speaker_info) # /data/0/train/speaker-info.txt
        # print(speaker_info)
        X_train.to_csv(speaker_info)
          
        
        # create files
        wav_scp = "wav.scp"
        wav_scp = pl.Path(kfold_dir_train / wav_scp)
        make_wav_scp(wav_files, X_train, file_path=wav_scp) # 1

        spk2utt = "spk2utt"
        spk2utt = pl.Path(kfold_dir_train / spk2utt)
        make_spk2utt(wav_dirs, X_train, file_path=spk2utt) # 2
        
        utt2spk = "utt2spk"
        utt2spk = pl.Path(kfold_dir_train / utt2spk)
        make_utt2spk(wav_dirs, X_train, file_path=utt2spk) # 3

        utt2accent = "utt2accent"
        utt2accent = pl.Path(kfold_dir_train / utt2accent) # data/0/train/utt2accent
        make_utt2accent(wav_dirs, X_train, file_path=utt2accent) # 4
        

        #####
        # validation
        #####
        kfold_dir_data = pl.Path("data")
        kfold_dir_data.mkdir(exist_ok=True)
        validation = "validation"
        speaker_info = "speaker-info.txt"
        kfold_dir_validation = pl.Path(kfold_dir_data / str(i) / validation)
        print(kfold_dir_validation)
        kfold_dir_validation.mkdir(parents=True, exist_ok=True)
        speaker_info = pl.Path(kfold_dir_validation / speaker_info)
        # print(speaker_info)
        X_validation.to_csv(speaker_info)
        
        # create files
        wav_scp = "wav.scp"
        wav_scp = pl.Path(kfold_dir_validation / wav_scp)
        make_wav_scp(wav_files, X_validation, file_path=wav_scp) # 1

        spk2utt = "spk2utt"
        spk2utt = pl.Path(kfold_dir_validation / spk2utt)
        make_spk2utt(wav_dirs, X_validation, file_path=spk2utt) # 2
        
        utt2spk = "utt2spk"
        utt2spk = pl.Path(kfold_dir_validation / utt2spk)
        make_utt2spk(wav_dirs, X_validation, file_path=utt2spk) # 3

        utt2accent = "utt2accent"
        utt2accent = pl.Path(kfold_dir_validation / utt2accent) # data/0/validation/utt2accent
        make_utt2accent(wav_dirs, X_validation, file_path=utt2accent) # 4
        

        #####
        # test
        #####
        kfold_dir_data = pl.Path("data")
        kfold_dir_data.mkdir(exist_ok=True)
        test = "test"
        speaker_info = "speaker-info.txt"
        kfold_dir_test = pl.Path(kfold_dir_data / str(i) / test)
        print(kfold_dir_test)
        kfold_dir_test.mkdir(parents=True, exist_ok=True)
        speaker_info = pl.Path(kfold_dir_test / speaker_info)
        # print(speaker_info)
        X_test.to_csv(speaker_info)

        # create files
        wav_scp = "wav.scp"
        wav_scp = pl.Path(kfold_dir_test / wav_scp)
        make_wav_scp(wav_files, X_test, file_path=wav_scp) # 1

        spk2utt = "spk2utt"
        spk2utt = pl.Path(kfold_dir_test / spk2utt)
        make_spk2utt(wav_dirs, X_test, file_path=spk2utt) # 2
        
        utt2spk = "utt2spk"
        utt2spk = pl.Path(kfold_dir_test / utt2spk)
        make_utt2spk(wav_dirs, X_test, file_path=utt2spk) # 3

        utt2accent = "utt2accent"
        utt2accent = pl.Path(kfold_dir_test / utt2accent) # data/0/test/utt2accent
        make_utt2accent(wav_dirs, X_test, file_path=utt2accent) # 4

# data_split_stratified_kfold(
#     spk_dataframe=test_spkr_info, 
#     wav_files=test_wav, 
#     wav_dirs=test_dir, 
#     stratify_using="ACCENTS", 
#     k_num_splits=1
#     )


def data_split_stratified_train_test(
    spk_dataframe,
    wav_files,
    wav_dirs,
    stratify_using="ACCENTS",
    train_percent=0.8,
    test_percent=0.2,
    k_num_splits=1, # default = 5

):  

    kfold_dir_data = pl.Path("data")
    kfold_dir_data.mkdir(exist_ok=True)

    speaker_info = "speaker-info.txt"
    train = "train"
    validation = "validation"
    test = "test"

    # variables  
    X = spk_dataframe
    y = X[stratify_using]
   
    einsof = 42 # random seed

    # first stratified K fold shuffle split of train and temp (i.e. dev/validation and test) sets

    skf = skms.StratifiedShuffleSplit(n_splits=k_num_splits, test_size=test_percent, random_state=einsof)
    skf = skf.split(X, y)

    for i, (train_index, test_index) in enumerate(skf):
        X_train = X.iloc[list(train_index), :]
        # y_train = y.iloc[list(train_index), :]
        X_test = X.iloc[list(test_index), :]
        
        X2 = X_test
        y2 = X2[stratify_using]

        #####
        # train
        #####
        kfold_dir_data = pl.Path("data")
        kfold_dir_data.mkdir(exist_ok=True)
        train = "train"
        speaker_info = "speaker-info.txt"
        kfold_dir_train = pl.Path(kfold_dir_data / str(i) / train) # /data/0/train
        # print(kfold_dir_train)
        kfold_dir_train.mkdir(parents=True, exist_ok=True)
        speaker_info = pl.Path(kfold_dir_train / speaker_info) # /data/0/train/speaker-info.txt
        # print(speaker_info)
        X_train.to_csv(speaker_info)
          
        
        # create files
        wav_scp = "wav.scp"
        wav_scp = pl.Path(kfold_dir_train / wav_scp)
        make_wav_scp(wav_files, X_train, file_path=wav_scp) # 1

        spk2utt = "spk2utt"
        spk2utt = pl.Path(kfold_dir_train / spk2utt)
        make_spk2utt(wav_dirs, X_train, file_path=spk2utt) # 2
        
        utt2spk = "utt2spk"
        utt2spk = pl.Path(kfold_dir_train / utt2spk)
        make_utt2spk(wav_dirs, X_train, file_path=utt2spk) # 3


        utt2accent = "utt2accent"
        utt2accent = pl.Path(kfold_dir_train / utt2accent) # data/0/train/utt2accent
        make_utt2accent(wav_dirs, X_train, file_path=utt2accent) # 4
        

        #####
        # test
        #####
        kfold_dir_data = pl.Path("data")
        kfold_dir_data.mkdir(exist_ok=True)
        test = "test"
        speaker_info = "speaker-info.txt"
        kfold_dir_test = pl.Path(kfold_dir_data / str(i) / test)
        print(kfold_dir_test)
        kfold_dir_test.mkdir(parents=True, exist_ok=True)
        speaker_info = pl.Path(kfold_dir_test / speaker_info)
        # print(speaker_info)
        X_test.to_csv(speaker_info)

        # create files
        wav_scp = "wav.scp"
        wav_scp = pl.Path(kfold_dir_test / wav_scp)
        make_wav_scp(wav_files, X_test, file_path=wav_scp) # 1

        spk2utt = "spk2utt"
        spk2utt = pl.Path(kfold_dir_test / spk2utt)
        make_spk2utt(wav_dirs, X_test, file_path=spk2utt) # 2
        
        utt2spk = "utt2spk"
        utt2spk = pl.Path(kfold_dir_test / utt2spk)
        make_utt2spk(wav_dirs, X_test, file_path=utt2spk) # 3

        utt2accent = "utt2accent"
        utt2accent = pl.Path(kfold_dir_test / utt2accent) # data/0/test/utt2accent
        make_utt2accent(wav_dirs, X_test, file_path=utt2accent) # 4


# data_split_stratified_kfold(
#     spk_dataframe=test_spkr_info, 
#     wav_files=test_wav, 
#     wav_dirs=test_dir, 
#     stratify_using="ACCENTS", 
#     k_num_splits=1
#     )

###
# this points to 
# - run_010_prepare
#  
# - 
#
###

def main():
    # directories
    vctk_root = "/export/corpora5/VCTK-Corpus"
    all = "/*"
    speaker_info = "/speaker-info.txt"
    text_files = "/txt"
    wave_files = "/wav48"
    current_dir = "."

    train_validation_split = "/data/0/train_proc_audio_no_sil"
    train_validation_split_output = "/data/0/train_proc_audio_no_sil/lists_xvec"

    

    # # files
    # test_wav = sorted(gl.glob(vctk_root + wave_files + all + all))
    # test_dir = sorted(gl.glob(vctk_root + wave_files + all))

    # # pre-prcessing of files 
    # # TODO: resolve - ParserError: Error tokenizing data. C error: Expected 5 fields in line 89, saw 6
    # # Skipping line 89: Expected 5 fields in line 89, saw 6. Error could possibly be due to quotes being ignored when a multi-char delimiter is used.
    # #   ID AGE GENDER ACCENTS REGION
    # #   326 26 M Australian English Sydney
    # test_spkr_info = pd.read_csv(
    #     vctk_root + speaker_info, delimiter="\s+", error_bad_lines=False, engine="python"
    # )

    # test_spkr_info_stats = test_spkr_info.info()
    # test_spkr_info_accent_cnts = test_spkr_info['ACCENTS'].value_counts()
    # ignore = ['SouthAfrican', 'Indian', 'Welsh', 'EnglishSE', 'Australian', 'EnglishSurrey', 'NewZealand']
    # test_spkr_info = test_spkr_info.query('ACCENTS != (@ignore)')

    # test_skf = data_split_stratified_kfold(
    #     spk_dataframe=test_spkr_info, 
    #     wav_files=test_wav, 
    #     wav_dirs=test_dir, 
    #     stratify_using="ACCENTS",
    #     train_percent=0.8, # use hyperion to split into train and validation - later in STEP 10
    #     validation_percent=0.0,
    #     test_percent=0.2, 
    #     k_num_splits=1) # doing one split for running hyperion pipeline

    test_skf = data_split_stratified_train_test(
        spk_dataframe=test_spkr_info, 
        wav_files=test_wav, 
        wav_dirs=test_dir, 
        stratify_using="ACCENTS",
        train_percent=0.8, # use hyperion to split into train and validation - later in STEP 10
        test_percent=0.2, 
        k_num_splits=1) # doing one split for running hyperion pipeline


if __name__ == '__main__':
    main()

# run the script on the grid.
# python -m make_vctk.py


# data/0/validation
# {293, 295, 264, 240, 306, 274, 276, 308, 246}

# data/0/test
# {256, 257, 258, 261, 262, 271, 278, 282, 285, 288, 303, 311, 312, 313, 315, 333, 360, 362, 236, 237}

# test >>> 
#        ID  AGE GENDER        ACCENTS           REGION
# 70   302   20      M       Canadian         Montreal
# 11   237   22      M       Scottish             Fife
# 73   305   19      F       American     Philadelphia
# 2    227   38      M        English          Cumbria
# 100  360   19      M       American        NewJersey
# 58   286   23      M        English        Newcastle
# 52   279   23      M        English        Leicester
# 57   285   21      M       Scottish        Edinburgh
# 67   299   25      F       American       California
# 33   260   21      M       Scottish           Orkney
# 47   274   22      M        English            Essex
# 77   310   21      F       American        Tennessee
# 71   303   24      F       Canadian          Toronto
# 31   258   22      M        English  SouthernEngland
# 74   306   21      F       American          NewYork
# 60   288   22      F          Irish           Dublin
# 9    234   22      F       Scottish     WestDumfries
# 104  364   23      M          Irish          Donegal
# 61   292   23      M  NorthernIrish          Belfast
# 4    229   23      F        English  SouthernEngland