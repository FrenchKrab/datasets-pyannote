# Generates URIs from filenames
FILES_SOURCE="wav/*.flac"
RESULT_DIR = "lists"

SEED=42

import glob
from pathlib import Path
import random
import sys
sys.path.append("../")


from scripts.uri import compute_uri_subsets_files, compute_uri_subsets_time
from scripts.io import write_stringlist_to_file


def is_aishell_test_file(filename: str):
    return filename.startswith('L') or filename.startswith('M') or filename.startswith('S')

def your_subset_creation_logic():
    # Original subsets
    all_uris = [Path(filename).stem for filename in glob.glob(FILES_SOURCE)]
    all_train_uris = [uri for uri in all_uris if not is_aishell_test_file(uri)]
    all_test_uris = [uri for uri in all_uris if is_aishell_test_file(uri)]

    write_stringlist_to_file(Path(RESULT_DIR) / "train.txt", all_train_uris)
    write_stringlist_to_file(Path(RESULT_DIR) / "test.txt", all_test_uris)

    # Custom subsets
    subsets_file_ratio = {'train_file85per':0.85, 'fr_file15per':0.15}
    subsets_time_ratio = {'train_time85per':0.85, 'dev_time15per':0.15}
        
    computed_subsets_uri = [
        compute_uri_subsets_files(all_train_uris, subsets_file_ratio, mode="ratio"),
        compute_uri_subsets_time(all_train_uris, subsets_time_ratio, mode="ratio")
    ]

    for computed_subsets in computed_subsets_uri:
        for subsetname, subseturis in computed_subsets.items():
            write_stringlist_to_file(Path(RESULT_DIR) / (subsetname+".txt"), subseturis)


if __name__ == '__main__':
    all_uris = [Path(filename).stem for filename in glob.glob(FILES_SOURCE)]
    write_stringlist_to_file(Path(RESULT_DIR) / "all.txt", all_uris, sort=True)

    if len(sys.argv) > 1 and sys.argv[1] == "index":
        print("Only created complete URIs index : all.txt")
        exit
    else:
        your_subset_creation_logic()