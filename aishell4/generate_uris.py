# Generates URIs from filenames
FILES_SOURCE="wav/*.flac"

# Subsets created from the training set, name:ratio_allocated
CUSTOM_TRAIN_SUBSETS = {'custom_train':0.8, 'custom_dev':0.2} 

RESULT_DIR = "lists"

SEED=42

import glob
from pathlib import Path
import random
import sys

sys.path.append("../")
from scripts.io import write_stringlist_to_file


def is_test_file(filename: str):
    return filename.startswith('L') or filename.startswith('M') or filename.startswith('S')

def get_subsets(uris: list, subsets: dict):
    rand = random.Random(SEED)
    uris_left = rand.sample(uris, len(uris))
    random.shuffle(uris_left)
    answer = {}
    for subsetname in subsets:
        ratio = subsets[subsetname]
        element_count = round(len(uris) * ratio)
        answer[subsetname] = uris_left[:element_count]
        uris_left = uris_left[element_count:]
    return answer


def main():
    all_uris = [Path(filename).stem for filename in glob.glob(FILES_SOURCE)]
    all_train_uris = [uri for uri in all_uris if not is_test_file(uri)]
    all_test_uris = [uri for uri in all_uris if is_test_file(uri)]

    custom_subsets = get_subsets(all_train_uris, CUSTOM_TRAIN_SUBSETS)
    for subsetname, subseturis in custom_subsets.items():
        write_stringlist_to_file(Path(RESULT_DIR) / (subsetname+".txt"), subseturis, sort=True)

    write_stringlist_to_file(Path(RESULT_DIR) / "original_train.txt", all_train_uris, sort=True)
    write_stringlist_to_file(Path(RESULT_DIR) / "test.txt", all_test_uris, sort=True)
    write_stringlist_to_file(Path(RESULT_DIR) / "all.txt", all_uris, sort=True)

if __name__ == '__main__':
    main()