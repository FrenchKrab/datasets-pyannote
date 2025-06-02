import argparse
from bisect import bisect_left
from pathlib import Path

import tqdm

from datasets_pyannote.io import get_files_in_paths
from datasets_pyannote.rttm import textgrid_to_annotation


def main():
    parser = argparse.ArgumentParser(description="Rename or deduplicate RTTM files to match other files.")
    parser.add_argument("inputs", type=str, help="input RTTM folder")
    parser.add_argument("variants", type=str, help="Matched files", nargs="+")
    parser.add_argument("output", type=str, help="output RTTM folder")
    parser.add_argument(
        "--variant-type",
        type=str,
        choices=["suffix"],
        help="How variants are constructed. Suffix means variant=URI+suffix",
        default="suffix",
    )

    args = parser.parse_args()

    inputs = get_files_in_paths([args.inputs], glob_pattern="*.rttm")
    variants = get_files_in_paths(args.variants, glob_pattern="*")
    variants_stem_to_path = {v.stem: v for v in variants}
    variants_stems = sorted(list(variants_stem_to_path.keys()))

    # find matches
    inputs_to_variant = {}
    for inputfile in tqdm.tqdm(inputs, desc="Finding matches"):
        inputs_to_variant[inputfile] = []

        if args.variant_type == "suffix":
            search_idx = bisect_left(variants_stems, inputfile.stem)
            search_done = False
            while search_idx < len(variants_stems) and not search_done:
                variant_stem = variants_stems[search_idx]
                if variant_stem.startswith(inputfile.stem):
                    inputs_to_variant[inputfile].append(variant_stem)
                else:
                    break
                search_idx += 1

    # Raise error if some inputs have no matches
    missing_matches = [inp for inp, variants in inputs_to_variant.items() if len(variants) == 0]
    if len(missing_matches) > 0:
        raise RuntimeError(f"Missing matches for files {';'.join([str(m) for m in missing_matches])}")

    # Copy files
    output_path = Path(args.output)
    output_path.mkdir(exist_ok=True, parents=True)
    for inputfile, variants in tqdm.tqdm(inputs_to_variant.items(), desc="Copying files"):
        for variant in variants:
            outputfile = output_path / (variant + inputfile.suffix)
            with open(inputfile, "r") as fin:
                with open(outputfile, "w") as fout:
                    for line in fin:
                        if inputfile.suffix.lower() == ".rttm":
                            splitted = line.split(" ", maxsplit=2)
                            splitted[1] = variant
                            line = " ".join(splitted)
                        fout.write(line)


if __name__ == "__main__":
    main()
