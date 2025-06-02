import contextlib
import sys
import wave
from typing import Literal

sys.path.append("../")
from scripts.io import read_stringlist_from_file
from scripts.uem import generate_uems_for_uris

UEM_OUT = "uems/"
URI_ALL = "lists/all.txt"
AUDIO_TEMPLATE = "wav/{uri}.wav"
RTTM_FOLDER = "rttm"

# none: dont use wavs
# safeguard: use wav duration to clip rttm if an annotation exceed file duration
# everything: use wave duration as uem
WAV_USE: Literal["none", "safeguard", "everything"] = "safeguard"


import glob
from pathlib import Path


def main():
    all_uris = read_stringlist_from_file(URI_ALL)
    generate_uems_for_uris(RTTM_FOLDER, UEM_OUT, all_uris, AUDIO_TEMPLATE, audio_use=WAV_USE)


if __name__ == "__main__":
    main()
