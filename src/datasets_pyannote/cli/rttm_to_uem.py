import argparse
from pathlib import Path

import tqdm
from pyannote.database.util import load_rttm

from datasets_pyannote.io import get_files_in_paths
from datasets_pyannote.uem import generate_uems_for_uris_v2


def main():
    parser = argparse.ArgumentParser(description="Generate UEMs from RTTMs")
    parser.add_argument("rttms", type=str, help="RTTM files/", nargs="+")
    parser.add_argument("uem_out", type=str, help="Output UEM file (if contains {uri} will generate one file per uri)")
    parser.add_argument(
        "--audio-template",
        type=str,
        help="Template for audio files, must contain {uri}, can be chained with ; (semicolums)",
        default=None,
    )
    parser.add_argument(
        "--start-strategy",
        type=str,
        help="How to handle the start time. zero = always 0.0, rttm=rttm start time",
        default="zero",
        choices=["zero", "rttm"],
    )
    parser.add_argument(
        "--end-strategy",
        type=str,
        help="How to handle the end time. audio=use audio duration, rttm_safe=use min(rttm, audio), rttm=use rttm",
        default=None,
        choices=["audio", "rttm_safe", "rttm"],
    )
    args = parser.parse_args()

    rttm_paths = get_files_in_paths(args.rttms, glob_pattern="*.rttm")
    rttms_dict = {}
    for rttm_path in tqdm.tqdm(rttm_paths, desc="Loading RTTMs"):
        rttms_dict.update(load_rttm(rttm_path))

    generate_uems_for_uris_v2(
        rttms_dict,
        args.uem_out,
        start_strategy=args.start_strategy,
        end_strategy=args.end_strategy,
        audio_path_template=args.audio_template,
    )


if __name__ == "__main__":
    main()
