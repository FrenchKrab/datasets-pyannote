# Dataset setup scripts for pyannote

This repository aims to centralize scripts that prepare datasets to be used with [pyannote-audio](https://github.com/pyannote/pyannote-audio) (more precisely, with its [pyannote-database](https://github.com/pyannote/pyannote-database) dependency).

Currently available : 
- [AISHELL4](aishell4)
- [AMI](ami)
- [AliMeeting](alimeeting)
- [MSDWild](msdwild)
- [MagicData-RAMC](ramc)
- [VoxConverse](voxconverse)
- [DIHARD-3 (no download)](dihard3)

Each dataset comes with its predefined `database.yml`, containing pyannote-database protocol(s) with already defined train+dev+test sets for out-of-the-box *speaker diarization* usage.
How these subsets are defined is entirely configurable.

The python package also contains utilitary cli scripts that can be used to setup the datasets.

## Installation

- Clone this repository
- Install the python package with `pip install -e .`
- To setup each dataset, refer to the `README.md` contained in their respective folder.

## FAQ

### How do I change the train/dev split / How do I define my own subsets ?

Head to the `generate_uris.py` of the desired dataset, and edit `your_subset_creation_logic()`, or find the `uri-subsets` command in the `setup.sh` script and edit it the same way (some standardization is still needed sorry).


This split can be absolute (= I want X files in subset1 / I want X hours in subset1) or relative (I want X% of the files in subset1 / I want X% of the hours in subset1).

Don't forget to update the database.yml file accordingly.
