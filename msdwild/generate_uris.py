from pathlib import Path
import random
import os

# Change this to configure !
# Here, the CUSTOM_FILES_SUBSET_MAPPING will split the few.train
# subset into a 'train' subset and a 'dev' subset, which are respectively
# 80% and 20% the size of the original subset.
# If you add a mapping, dont forget to append it to ALL_FILE_SUBSETS_TO_PROCESS
OG_FILE_SUBSET_MAPPING = {
    "few.train.rttm" : {'few_train':1.0},
    "few.val.rttm" : {'few_val': 1.0},
    "many.val.rttm" : {'many_val': 1.0},
}
CUSTOM_FILES_SUBSET_MAPPING = {
    "few.train.rttm" : {'train':0.8, 'dev':0.2},
    "few.val.rttm" : {'test': 1.0},
    "many.val.rttm" : {'test_many': 1.0}
}
ALL_FILE_SUBSETS_TO_PROCESS = [OG_FILE_SUBSET_MAPPING, CUSTOM_FILES_SUBSET_MAPPING]


OUTDIR = "lists"
SEED=42


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

def get_all_subset_uris_in_rttm(file_subset_mapping: dict) -> dict:
    uris = {}
    for file in file_subset_mapping:

        uris_in_file = set()
        with open(file, 'r') as f:
            for line in f:
                splitted = line.split(' ')
                uri = splitted[1]
                uris_in_file.add(uri)
        subset_uris = get_subsets(list(uris_in_file), file_subset_mapping[file])
        for subset in subset_uris:
            if subset not in uris:
                uris[subset] = []
            uris[subset] += subset_uris[subset]

    # make sure there's only one occurence of the uri in each subset
    for subset in uris:
        uris[subset] = list(set(uris[subset]))
    return uris

def write_stringlist_to_file(filepath:str, stringlist:list, sort=False):
    if sort:
        stringlist.sort()
    file_to_write_path = Path(filepath)
    file_to_write_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_to_write_path, 'w') as f:
        for s in stringlist:
            f.write(s+"\n")



def main():
    for file_subset_mapping in ALL_FILE_SUBSETS_TO_PROCESS:
        subsets_uris = get_all_subset_uris_in_rttm(file_subset_mapping)
        for subset, uris in subsets_uris.items():
            write_stringlist_to_file(os.path.join(OUTDIR, f"{subset}.txt"), uris)


if __name__ == "__main__":
    main()