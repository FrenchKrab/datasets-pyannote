import math
import os
import random
import sys
from multiprocessing.sharedctypes import Value
from pathlib import Path
from typing import Literal

sys.path.append("../")
from scripts.io import write_stringlist_to_file
from scripts.uri import compute_uri_subsets_files, compute_uri_subsets_time

ALL_FILES_MAPPING = {
    "few.train.rttm": {"all": 1.0},  # 2476 files, 65h54
    "few.val.rttm": {"all": 1.0},  # 490 files, 9h49
    "many.val.rttm": {"all": 1.0},  # 177 files, 4h04
}


UEM_TEMPLATE = "uems/{uri}.uem"
OUTDIR = "lists"
SEED = 42


def get_all_subset_uris_in_rttm(
    file_subset_mapping: dict, unit: Literal["time", "file"], mode: Literal["ratio", "absolute"]
) -> dict:
    uris = {}
    for file in file_subset_mapping:
        uris_in_file = set()
        with open(file, "r") as f:
            for line in f:
                splitted = line.split(" ")
                uri = splitted[1]
                uris_in_file.add(uri)
        if unit == "file":
            subset_uris = compute_uri_subsets_files(list(uris_in_file), file_subset_mapping[file], mode=mode, seed=SEED)
        elif unit == "time":
            subset_uris = compute_uri_subsets_time(
                list(uris_in_file), UEM_TEMPLATE, file_subset_mapping[file], mode=mode, seed=SEED
            )
        else:
            raise ValueError(f"unknown unit : {unit}")

        for subset in subset_uris:
            if subset not in uris:
                uris[subset] = []
            uris[subset] += subset_uris[subset]

    # make sure there's only one occurence of the uri in each subset
    for subset in uris:
        uris[subset] = list(set(uris[subset]))
    return uris


def your_subset_creation_logic():
    # Change this to configure !
    OG_FILE_SUBSET_MAPPING = {
        "few.train.rttm": {"few_train": 1.0},
        "few.val.rttm": {"few_val": 1.0},
        "many.val.rttm": {"many_val": 1.0},
    }
    CUSTOM_FILES_SUBSET_MAPPING = {
        "few.train.rttm": {
            "custom1_dev": 60 * 60 * 6,
            "custom1_train": +math.inf,
        },  # put 6h into 'dev', the rest into 'train'
    }

    all_subsets = [
        get_all_subset_uris_in_rttm(OG_FILE_SUBSET_MAPPING, "file", "ratio"),
        get_all_subset_uris_in_rttm(CUSTOM_FILES_SUBSET_MAPPING, "time", "absolute"),
    ]

    for subsets_uris in all_subsets:
        for subset, uris in subsets_uris.items():
            write_stringlist_to_file(os.path.join(OUTDIR, f"{subset}.txt"), uris)


if __name__ == "__main__":
    # write the "all.txt" file indexing all uris
    all_subset_uris = get_all_subset_uris_in_rttm(ALL_FILES_MAPPING, "file", "ratio")["all"]
    write_stringlist_to_file(os.path.join(OUTDIR, f"all.txt"), all_subset_uris)

    if len(sys.argv) > 1 and sys.argv[1] == "index":
        print("Only created complete URIs index : all.txt")
        exit
    else:
        your_subset_creation_logic()
