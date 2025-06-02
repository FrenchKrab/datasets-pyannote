import math
import sys

sys.path.append("../")
import glob
from pathlib import Path

from datasets_pyannote.io import write_stringlist_to_file
from datasets_pyannote.uem import generate_uems_for_uris
from datasets_pyannote.uri import compute_uri_subsets_time


def main():

    # ---- generate URI files
    uris_dev = []
    uris_test = []

    for rttm_file in glob.glob("rttm/dev/*.rttm"):
        uris_dev.append(Path(rttm_file).stem)
    for rttm_file in glob.glob("rttm/test/*.rttm"):
        uris_test.append(Path(rttm_file).stem)

    write_stringlist_to_file("uris/dev.txt", uris_dev)
    write_stringlist_to_file("uris/test.txt", uris_test)

    # ---- generate UEMs
    generate_uems_for_uris(
        rttm_folder="rttm/dev/",
        out_folder="uem/dev",
        uris=uris_dev,
        audio_path_template="wav/{uri}.wav",
        audio_use="everything",
    )

    generate_uems_for_uris(
        rttm_folder="rttm/test/",
        out_folder="uem/test",
        uris=uris_test,
        audio_path_template="wav/{uri}.wav",
        audio_use="everything",
    )

    # --- Generate custom URI files to split 'dev' into train/val (2h val set) ---
    custom1 = compute_uri_subsets_time(
        uris=uris_dev,
        uem_template="uem/dev/{uri}.uem",
        subsets={"val": 3600 * 2, "train": math.inf},
        mode="absolute",
    )
    for subsetname in custom1:
        write_stringlist_to_file(f"uris/custom1/dev_{subsetname}.txt", custom1[subsetname])


if __name__ == "__main__":
    main()
