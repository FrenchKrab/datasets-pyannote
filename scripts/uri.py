
import random


def compute_uri_subsets_files(uris: list, subsets: dict, seed=42) -> dict:
    """Splits a list of URI into multiple subsets, following ratios for the number of files in each subset.

    Parameters
    ----------
    uris : list
        List of URIs
    subsets : dict
        Subset distribution; eg {'subset1':0.2,'subset2':0.3,'subset3':0.5}
        Values should sum to 1.0
    seed : int, optional
        Seed to use for random shuffling, by default 42

    Returns
    -------
    dict
        Dictionary mapping subset names to their lists of URIs
    """

    rand = random.Random(seed)
    uris_left = rand.sample(uris, len(uris))
    random.shuffle(uris_left)
    answer = {}
    for subsetname in subsets:
        ratio = subsets[subsetname]
        element_count = round(len(uris) * ratio)
        answer[subsetname] = uris_left[:element_count]
        uris_left = uris_left[element_count:]
    return answer