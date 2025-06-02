from pathlib import Path

import textgrid
from pyannote.core import Annotation, Segment, Timeline


def get_time_data_from_rttm(rttm_file: str) -> dict:
    data = {}
    with open(rttm_file, "r") as f:
        data["latest_time"] = 0.0
        data["earliest_time"] = 99999999999.0
        for line in f:
            splitted = line.split(" ")
            if len(splitted) < 4:
                continue
            time_begin = float(splitted[3])
            time_duration = float(splitted[4])
            data["latest_time"] = max(data["latest_time"], time_begin + time_duration)
            data["earliest_time"] = min(data["earliest_time"], time_begin)
    return data


def textgrid_to_annotation(textgrid_file: str) -> Annotation:
    tg = textgrid.TextGrid.fromFile(textgrid_file)

    # list of tuples with the segment, track and label
    records: list[tuple[Segment, str, str]] = []
    for tier in tg.tiers:
        for interval in tier.intervals:
            records.append((Segment(interval.minTime, interval.maxTime), tier.name, tier.name))
    annotation = Annotation.from_records(records, uri=Path(textgrid_file).stem)

    return annotation
