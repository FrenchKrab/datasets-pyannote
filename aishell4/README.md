# AISHELL-4 for Pyannote

These scripts automatically download the AISHELL-4 dataset and set it up to be used with pyannote-database.

It will generate two subsets of the original training data : 'train' and 'dev', as the original dataset only has training and test data (defaults are 80% train files, 20% dev files).

## Instruction

Run `setup.sh` to download and extract the files.

If you want to change the subsets generated from the original training dataset, change the `CUSTOM_TRAIN_SUBSETS` variable in `generate_uris.py` and run `python generate_uris.py`. If you add/remove subsets, don't forget to edit database.yml accordingly.

## Original sets info

| subset | # files | total length |
|---|----|----|
| train | 191 | 104h46m |
| test | 20 | 12h34m |

## Credits

- AISHELL-4 (CC BY-SA 4.0) : 
    - Dataset: https://www.openslr.org/111/
    - Original website : http://www.aishelltech.com/aishell_4