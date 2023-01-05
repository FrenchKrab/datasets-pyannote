
from operator import sub
import random
from typing import List, Literal, Text

from scripts.uem import get_uem_data_uris


def compute_uri_subsets_files(uris: list, subsets: dict, mode: Literal['ratio','absolute'], seed=42) -> dict:
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
        if mode == 'ratio':
            ratio = subsets[subsetname]
            element_count = round(len(uris) * ratio)
        elif mode == 'absolute':
            element_count = subsets[subsetname]
        else:
            raise ValueError(f"Invalid mode : {mode}")


        answer[subsetname] = uris_left[:element_count]
        uris_left = uris_left[element_count:]
    return answer

def compute_uri_subsets_time(uris: List[Text], uem_template: str, subsets: dict[str,float], mode: Literal['ratio','absolute'], seed=42):
    """Divides a list of URIs into disjoint subsets of a certain duration (either relative to the total URIs duration, or absolute time).

    Parameters
    ----------
    uris : List[Text]
        List of URIs to divide into subsets
    uem_template : str
        Template where to find uem files. eg 'uems/{uri}.uem'
    subsets : dict[str,float]
        Mapping of subset names to a float, see 'mode' for the float meaning.
    mode : Literal['ratio','absolute']
        Either
        -   ratio: a float in [0,1], sum of all float should be at most 1.
            {"s1":0.8,"s2":0.2} means we want 80% of the URIs time to be
            in subset s1, and 20% in subset s2.
        -   absolute: a float in [0,total duration of the URIs].
            In this case, the float represents the desired subset duration in SECONDS.
    seed : int, optional
        Seed for the URIs random shuffle, by default 42

    Returns
    -------
    dict
        Dictionary mapping subset names to their lists of URIs

    Raises
    ------
    Exception
        In case the desired subset distribution is impossible (we're left with at least one empty subset).
    """

    files_duration, total_time = get_uem_data_uris(uris, uem_template)
    
    # compute subsets
    rand = random.Random(seed)
    uris_left = rand.sample(uris, len(uris))
    random.shuffle(uris_left)
    answer = {}

    for subsetname in subsets:
        if mode == 'ratio':
            ratio = subsets[subsetname]
            seconds_left_to_fill = ratio * total_time
        elif mode == 'absolute':
            seconds_left_to_fill = subsets[subsetname]
        else:
            raise ValueError(f"Invalid mode : {mode}")
        subset_content = []

        while len(uris_left) > 0 and seconds_left_to_fill > 0:
            picked_uri, uris_left = uris_left[0], uris_left[1:]
            subset_content.append(picked_uri)
            picked_time = files_duration[picked_uri]
            seconds_left_to_fill -= picked_time

        if len(subset_content) == 0:
            raise Exception(f"There's not enough data left for the {subsetname} subset !")
        answer[subsetname] = subset_content
    return answer