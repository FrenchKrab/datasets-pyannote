# Generates URIs from filenames
FILES_SOURCE="wav/*.flac"

# Subsets created from the training set, name:ratio_allocated
CUSTOM_TRAIN_SUBSETS = {'train':0.8, 'dev':0.2} 

RESULT_DIR = "lists"


import glob
from pathlib import Path
import random


def is_test_file(filename: str):
    return filename.startswith('L') or filename.startswith('M') or filename.startswith('S')

def get_subsets(uris: list, subsets: dict):
    uris_left = uris.copy()
    random.shuffle(uris_left)
    answer = {}
    for subsetname in subsets:
        ratio = subsets[subsetname]
        element_count = round(len(uris) * ratio)
        answer[subsetname] = uris_left[:element_count]
        uris_left = uris_left[element_count:]
    return answer

def get_filenames(pattern: str):
    all_uris = []
    for filename in glob.glob(pattern):
        uri = Path(filename).stem
        all_uris.append(uri)
    return all_uris

def write_stringlist_to_file(filepath:str, stringlist:list, sort=False):
    if sort:
        stringlist.sort()
    file_to_write_path = Path(filepath)
    file_to_write_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_to_write_path, 'w') as f:
        for s in stringlist:
            f.write(s+"\n")

def main():
    all_uris = get_filenames(FILES_SOURCE)
    all_train_uris = [uri for uri in all_uris if not is_test_file(uri)]
    all_test_uris = [uri for uri in all_uris if is_test_file(uri)]

    custom_subsets = get_subsets(all_train_uris, CUSTOM_TRAIN_SUBSETS)
    for subsetname, subseturis in custom_subsets.items():
        write_stringlist_to_file(Path(RESULT_DIR) / (subsetname+".txt"), subseturis, sort=True)

    write_stringlist_to_file(Path(RESULT_DIR) / ("test.txt"), all_test_uris, sort=True)

if __name__ == '__main__':
    main()