# AISHELL-4 for Pyannote

These scripts automatically download the AISHELL-4 dataset and set it up to be used with pyannote-database.

It will generate two subsets from the original `train` set : `custom_train` and `custom_dev`, as the original dataset only has training and test data.
Defaults are 12h for `custom_dev`, and what's left (~92h) for `custom_train`.

Out-of-the-box protocol for pyannote.audio training is `AISHELL.SpeakerDiarization.Custom`.

## Instruction

Run `setup.sh` to download and extract the files.


## Original sets info

| subset | # files | total length |
|---|----|----|
| train | 191 | 104h46m |
| test | 20 | 12h34m |

## Credits

- AISHELL-4 (CC BY-SA 4.0) : 
    - Dataset: https://www.openslr.org/111/
    - Original website : http://www.aishelltech.com/aishell_4