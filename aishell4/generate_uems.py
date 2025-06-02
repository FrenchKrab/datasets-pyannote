UEM_OUT = "uems/"
ALL_URIS_FILE = "lists/all.txt"
RTTM_FOLDER = "rttm"

import sys

sys.path.append("../")
from datasets_pyannote.io import read_stringlist_from_file
from datasets_pyannote.uem import generate_uems_for_uris


def main():
    all_uris = read_stringlist_from_file(ALL_URIS_FILE)
    generate_uems_for_uris(RTTM_FOLDER, UEM_OUT, all_uris)


if __name__ == "__main__":
    main()
