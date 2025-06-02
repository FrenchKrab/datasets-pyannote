# Generates URIs from filenames
FILES_SOURCE = "wav/*.flac"
RESULT_DIR = "lists"
UEM_TEMPLATE = "uems/{uri}.uem"

SEED = 42

import glob
import math
import random
import sys
from pathlib import Path

sys.path.append("../")


from scripts.io import write_stringlist_to_file
from scripts.uri import compute_uri_subsets_files, compute_uri_subsets_time


def is_aishell_test_file(filename: str):
    return filename.startswith("L") or filename.startswith("M") or filename.startswith("S")


def your_subset_creation_logic():
    # Original subsets
    all_uris = [Path(filename).stem for filename in glob.glob(FILES_SOURCE)]
    all_train_uris = [uri for uri in all_uris if not is_aishell_test_file(uri)]  # 191 files, 104h46m
    all_test_uris = [uri for uri in all_uris if is_aishell_test_file(uri)]  # 20 files, 12h34m

    write_stringlist_to_file(Path(RESULT_DIR) / "train.txt", all_train_uris)
    write_stringlist_to_file(Path(RESULT_DIR) / "test.txt", all_test_uris)

    # Custom subsets !
    subsets_time_ratio = {
        "custom_dev": 60 * 60 * 12.0,
        "custom_train": math.inf,
    }  # aim for about the same size as test : 12h

    computed_subsets_uri = [compute_uri_subsets_time(all_train_uris, UEM_TEMPLATE, subsets_time_ratio, mode="absolute")]

    for computed_subsets in computed_subsets_uri:
        for subsetname, subseturis in computed_subsets.items():
            write_stringlist_to_file(Path(RESULT_DIR) / (subsetname + ".txt"), subseturis)


if __name__ == "__main__":
    all_uris = [Path(filename).stem for filename in glob.glob(FILES_SOURCE)]
    write_stringlist_to_file(Path(RESULT_DIR) / "all.txt", all_uris, sort=True)

    if len(sys.argv) > 1 and sys.argv[1] == "index":
        print("Only created complete URIs index : all.txt")
        exit
    else:
        your_subset_creation_logic()
