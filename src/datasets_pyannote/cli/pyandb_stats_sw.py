import argparse
from pathlib import Path
import pandas as pd
import tqdm
from pyannote.database import registry, ProtocolFile
from pyannote.core import Annotation, Timeline, Segment
import numpy as np
import torch


def compute_distrib_stats(values: list[float], prefix: str = "") -> dict:
    return {
        prefix + "min": np.min(values),
        prefix + "max": np.max(values),
        prefix + "mean": np.mean(values),
        prefix + "median": np.median(values),
        prefix + "sum": np.sum(values),
    }


def compute_discrete_histogram(values: list[float], prefix: str = "") -> dict:
    d = {}
    unique_values = np.unique(values)
    for value in unique_values:
        d[prefix + str(value)] = np.sum(values == value) / len(values) * 100
    return d


def accumulate_stats_on_files(
    files: list[ProtocolFile],
    dataset_name: str = "",
    ann_sr: float = 50.0,
    sw_sizes: list[float] = [5.0, 10.0],
    sw_step: float = 1.0,
    sw_min_uem_ratio: float = 0.8,
) -> dict:
    stats = {
        "num_files": len(files),
        "file_duration": [],
    }
    stats.update({
        f'sw_{sw_size:.0f}.speaker_count': []
        for sw_size in sw_sizes
    })
    stats.update({
        f'sw_{sw_size:.0f}.windows': 0
        for sw_size in sw_sizes
    })

    for file in tqdm.tqdm(files, desc=f"Computing stats on {dataset_name}"):
        uem: Timeline = file["annotated"].support()
        ann: Annotation = file["annotation"]
        stats["file_duration"].append(uem.duration())


        extent_support = ann.support().get_timeline().extent() | uem.support().extent()
        # (Frames, Speakers)
        ann_arr = torch.from_numpy(ann.discretize(resolution=1 / ann_sr, support=extent_support).data)
        # (Frames, 1)
        uem_arr = torch.from_numpy(uem.to_annotation().discretize(resolution=1 / ann_sr, support=extent_support).data).sum(dim=1, keepdim=True)

        if (uem_arr > 1).any():
            raise RuntimeError("Something went wrong.")

        for sw_size in sw_sizes:
            sw_size_frames = round(sw_size * ann_sr)
            sw_step_frames = round(sw_step * ann_sr)

            
            if ann_arr.shape[0] < sw_size_frames:
                padded_ann_arr = torch.nn.functional.pad(ann_arr, (0, 0, 0, sw_size_frames - ann_arr.shape[0]))
                padded_uem_arr = torch.nn.functional.pad(uem_arr, (0, 0, 0, sw_size_frames - uem_arr.shape[0]))
            else:
                padded_ann_arr = ann_arr
                padded_uem_arr = uem_arr

            # (Windows, Frames, Speakers)
            ann_sw = padded_ann_arr.unfold(0, sw_size_frames, sw_step_frames).swapaxes(1,2)
            # (Windows, Frames, 1)
            uem_sw = padded_uem_arr.unfold(0, sw_size_frames, sw_step_frames).swapaxes(1,2)
    

            # (Windows,)
            valid_windows = uem_sw[...,0].sum(dim=1) > (sw_size_frames * sw_min_uem_ratio)

            # sum spk activity on the time dim, then clamp it to 1, then sum on the speaker dim (total spk per window)
            # (Windows,)
            spk_per_windows = (ann_sw * uem_sw).sum(dim=1).clamp(max=1.0).sum(dim=1)
            stats[f'sw_{sw_size:.0f}.speaker_count'] += spk_per_windows[valid_windows].numpy().tolist()
            stats[f'sw_{sw_size:.0f}.windows'] += valid_windows.sum().item()

    return stats


def main():
    parser = argparse.ArgumentParser(description="Generate stats about pyannote database protocols")
    parser.add_argument("--protocols", type=str, help="List of protocols in format A.Task.B", nargs="+", required=True)
    parser.add_argument(
        "--subsets", type=str, nargs="+", choices=["train", "development", "test"], help="Which subsets to include"
    )
    parser.add_argument(
        "--ann-sr", type=float, help="Sampling rate of annotations to compute framewise statistics.", default=50.0
    )
    parser.add_argument(
        "--sw_size", type=float, nargs="+", help="List of sliding window sizes in seconds.", default=[5.0, 10.0]
    )
    parser.add_argument("--sw_step", type=float, help="Sliding window stride in seconds.", default=1.0)
    parser.add_argument("--sw_min_uem_ratio", type=float, help="Minimum UEM ratio for a sliding window to be counted in stats.", default=0.5)
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
                    list(subsetmethod()),
                    f"{protocolname}.{subsetname}",
                    ann_sr=args.ann_sr,
                    sw_sizes=args.sw_size,
                    sw_step=args.sw_step,
                    sw_min_uem_ratio=args.sw_min_uem_ratio
                )

    stats: dict[tuple[str, str], dict] = {}
    for (protocolname, subsetname), acc in accumulated_stats.items():
        this_stats = {
            "num_files": acc["num_files"],
        }
        this_stats.update(compute_distrib_stats(acc["file_duration"], "file_duration."))
        for sw_size in args.sw_size:
            this_stats.update(compute_distrib_stats(acc[f'sw_{sw_size:.0f}.speaker_count'], f'sw_{sw_size:.0f}.speaker_count.'))
            this_stats[f'sw_{sw_size:.0f}.windows'] = acc[f'sw_{sw_size:.0f}.windows']

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
