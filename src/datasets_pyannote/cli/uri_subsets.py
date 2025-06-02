import argparse
from pathlib import Path

from datasets_pyannote.io import read_stringlist_from_file, write_stringlist_to_file
from datasets_pyannote.uri import compute_uri_subsets_files, compute_uri_subsets_time


def parse_subsets(subsets_strlist):
    subsets = {}

    for i in range(0, len(subsets_strlist), 2):
        subsetname = subsets_strlist[i]
        value = float(subsets_strlist[i + 1])
        if value <= -1:
            value = 3600 * 100000
        subsets[subsetname] = value
    return subsets


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("split", type=str, choices=["time", "file"], help="Use time or file count for creating subsets")
    parser.add_argument(
        "mode",
        type=str,
        choices=["ratio", "absolute"],
        help="Specify as ratio of total time/files or absolute time/file count",
    )
    parser.add_argument("uris", type=str, nargs="+", help="Files containing list of URIs")
    parser.add_argument(
        "--subsets", nargs="+", type=str, help="Subsets to create format 'subset1 0.25 subset2 0.5 subset3 -1'"
    )
    parser.add_argument("--output", type=str, help="Output folder to write subsets")
    parser.add_argument("--uem", type=str, help="UEM file/template to use for time based subsets")
    parser.add_argument("--seed", type=int, default=42, help="Seed for random shuffling")
    parser.add_argument("--verbose", action="store_true", help="Print verbose output")

    args = parser.parse_args()

    uris = []
    for uri_file in args.uris:
        uris.extend(read_stringlist_from_file(uri_file))
    uris = list(set(uris))

    subsets = parse_subsets(args.subsets)
    if args.split == "time":
        if args.uem is None:
            raise ValueError("UEM file/template is required for time based subsets")
        result = compute_uri_subsets_time(
            uris=uris, uem_template=args.uem, subsets=subsets, mode=args.mode, seed=args.seed, verbose=args.verbose
        )
        for subset, uris in result.items():
            write_stringlist_to_file(Path(args.output) / f"{subset}.txt", uris, sort=True)
    elif args.split == "file":
        result = compute_uri_subsets_files(
            uris=uris, subsets=subsets, mode=args.mode, seed=args.seed, verbose=args.verbose
        )
        for subset, uris in result.items():
            write_stringlist_to_file(Path(args.output) / f"{subset}.txt", uris, sort=True)
    else:
        raise ValueError(f"Invalid split: {args.mode}")


if __name__ == "__main__":
    main()
