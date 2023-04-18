# Dataset setup scripts for pyannote

This repository aims to centralize scripts that prepare datasets to be used with [pyannote-audio](https://github.com/pyannote/pyannote-audio) (more precisely, with its [pyannote-database](https://github.com/pyannote/pyannote-database) dependency).

Currently available : 
- [AISHELL4](aishell4)
- [MSDWild](msdwild)
- [VoxCeleb](voxceleb)

To setup each dataset, refer to the `README.md` contained in their respective folder.

Each dataset comes with its predefined `database.yml`, containing pyannote-database protocol(s) with already defined train+dev+test sets for out-of-the-box *speaker diarization* usage.
How these subsets are defined is entirely configurable.

## FAQ
### How do I change the train/dev split / How do I define my own subsets ?

Head to the `generate_uris.py` of the desired dataset, and edit `your_subset_creation_logic()`.
In particular check `compute_uri_subsets_files(...)` and `compute_uri_subsets_time(...)` in [scripts/uri.py](scripts/uri.py), which allow you to split according to the number of files or time desired in the subsets. 

This split can be absolute (= I want X files in subset1 / I want X hours in subset1) or relative (I want X% of the files in subset1 / I want X% of the hours in subset1).

Don't forget to update the database.yml file accordingly.