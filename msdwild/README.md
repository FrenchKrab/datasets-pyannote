# MSDWild for Pyannote

This repository automatically downloads the MSDWILD dataset and set it up to be used with [pyannote-database](https://github.com/pyannote/pyannote-database).


It will generate two subsets from the original `few.train` set : `custom1_train` and `custom1_dev`, as the original dataset only has training and test data.
Defaults are 6h for `custom1_dev`, and what's left (~60h) for `custom1_train`.

Out-of-the-box protocol for pyannote.audio training is `MSDWILD.SpeakerDiarization.CustomFew`.

## Instructions

Clone this repository, download the dataset zip at https://github.com/X-LANCE/MSDWILD#wavs and put it under the `msdwild` folder.
Then, run `setup.sh` in the `msdwild` directory to download/extract/generate the files (wav, rttm, uem, uris).


## Original sets info

| subset | # files | total length |
|---|----|----|
| few.train | 2476 | 65h54m |
| few.val | 490 | 9h49m |
| many.val | 177 | 4h04 |

## Credits

- [MSDWild](https://github.com/X-LANCE/MSDWILD)