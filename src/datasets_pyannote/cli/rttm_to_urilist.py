import argparse
import sys
from pathlib import Path

import tqdm

sys.path.append("../")
from datasets_pyannote.io import write_stringlist_to_file


def main():

    parser = argparse.ArgumentParser(description="Convert RTTM file or directory to list of URIs")
    parser.add_argument("input", type=str, help="input RTTM file / directory")
    parser.add_argument("output", type=str, help="output URI file")

    args = parser.parse_args()

    # Determine the input(s)
    input_path = Path(args.input)
    if input_path.is_dir():
        rttm_files = list(input_path.glob("*.rttm"))
    else:
        rttm_files = [input_path]

    # read URIs from RTTMs
    uris = set()
    for rttm_fpath in tqdm.tqdm(rttm_files, desc="Retrieving URIs from RTTM files"):
        with open(rttm_fpath, "r") as f:
            for line in f:
                splitted = line.split(" ", maxsplit=2)
                uris.add(splitted[1])

    # Write result
    write_stringlist_to_file(args.output, list(uris), sort=True)


if __name__ == "__main__":
    main()
