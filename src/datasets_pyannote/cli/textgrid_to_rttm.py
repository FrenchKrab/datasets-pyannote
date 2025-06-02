import argparse
import sys
from pathlib import Path

import tqdm

from datasets_pyannote.io import get_files_in_paths
from datasets_pyannote.rttm import textgrid_to_annotation


def main():
    parser = argparse.ArgumentParser(description="Convert TextGrid to RTTM")
    parser.add_argument("inputs", type=str, help="input TextGrid file(s) / folder", nargs="+")
    parser.add_argument("output", type=str, help="output RTTM folder")
    args = parser.parse_args()

    textgrid_files = get_files_in_paths(args.inputs, glob_pattern="*.TextGrid")

    output_path = Path(args.output)
    output_path.mkdir(exist_ok=True, parents=True)
    for textgrid_file in tqdm.tqdm(textgrid_files, desc="Converting TextGrid files to RTTM"):
        annotation = textgrid_to_annotation(str(textgrid_file))
        rttm_file = output_path / (textgrid_file.stem + ".rttm")
        with open(rttm_file, "w") as f:
            annotation.write_rttm(f)


if __name__ == "__main__":
    main()
