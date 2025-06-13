import argparse
from pathlib import Path
import pandas as pd
import tqdm
from pyannote.database import registry, ProtocolFile
from pyannote.core import Annotation, Timeline, Segment
import numpy as np


def compute_distrib_stats(values: list[float], prefix: str = "") -> dict:
    return {
        prefix + "min": np.min(values),
        prefix + "max": np.max(values),
        prefix + "mean": np.mean(values),
        prefix + "median": np.median(values),
    }


def accumulate_stats_on_files(files: list[ProtocolFile], dataset_name: str = "") -> dict:
    stats = {
        "num_files": len(files),
        "speaker_count": [],
        "file_duration": [],
        "speech_duration": [],
        "ov_duration": [],
    }

    for file in tqdm.tqdm(files, desc=f"Computing stats on {dataset_name}"):
        uem: Timeline = file["annotated"]
        ann: Annotation = file["annotation"]

        stats["speaker_count"].append(len(ann.labels()))
        stats["file_duration"].append(uem.duration())
        stats["speech_duration"].append(ann.get_timeline().support().duration())
        stats["ov_duration"].append(ann.get_overlap().support().duration())

    return stats


def main():
    parser = argparse.ArgumentParser(description="Generate stats about pyannote database protocols")
    parser.add_argument("--protocols", type=str, help="List of protocols in format A.Task.B", nargs="+", required=True)
    parser.add_argument(
        "--subsets", type=str, nargs="+", choices=["train", "development", "test"], help="Which subsets to include"
    )
    parser.add_argument("--database_yml", type=str, nargs="+", help="Path to database.yml files to load")
    parser.add_argument("--output", type=str, help="Output file, leave empty to print to stdout", default=None)
    args = parser.parse_args()

    for databaseyml in args.database_yml:
        registry.load_database(databaseyml)

    # (protocolname, subsetname) -> stats_dict
    accumulated_stats: dict[tuple[str, str], dict] = {}

    for protocolname in args.protocols:
        protocol = registry.get_protocol(protocolname)
        for subsetname in args.subsets:
            # try loading the subset
            subsetmethod = getattr(protocol, subsetname, None)
            if subsetmethod is not None:
                accumulated_stats[(protocolname, subsetname)] = accumulate_stats_on_files(
                    list(subsetmethod()), f"{protocolname}.{subsetname}"
                )

    stats: dict[tuple[str, str], dict] = {}
    for (protocolname, subsetname), acc in accumulated_stats.items():
        this_stats = {
            "num_files": acc["num_files"],
        }
        this_stats.update(compute_distrib_stats(acc["speaker_count"], "speaker_count."))
        this_stats.update(compute_distrib_stats(acc["file_duration"], "file_duration."))
        this_stats.update(compute_distrib_stats(acc["speech_duration"], "speech_duration."))
        this_stats.update(compute_distrib_stats(acc["ov_duration"], "ov_duration."))

        speech_ratio = np.array(acc["speech_duration"]) / np.array(acc["file_duration"])
        this_stats.update(compute_distrib_stats(speech_ratio * 100, "speech_percent."))

        ov_ratio = np.array(acc["ov_duration"]) / np.array(acc["file_duration"])
        this_stats.update(compute_distrib_stats(ov_ratio * 100, "ov_percent."))

        stats[(protocolname, subsetname)] = this_stats

    df = pd.DataFrame.from_dict(stats, orient="index")
    # rename index
    df.index.set_names(["protocol", "subset"], inplace=True)

    if ".md" in args.output:
        df.to_markdown(args.output)
    if args.output is not None:
        df.to_csv(args.output)
    else:
        print(df.to_csv())


if __name__ == "__main__":
    main()
