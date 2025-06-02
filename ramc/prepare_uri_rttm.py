import re
from pathlib import Path

from pyannote.core import Annotation, Segment

from datasets_pyannote.io import write_stringlist_to_file

PARTITIONS = ["train", "dev", "test"]

OG_DATAPARTITIONS_FOLDER = Path("DataPartition")
LISTS_FOLDER = Path("lists")

OG_ANNOTATIONS_FOLDER = Path("MDT2021S003/TXT")
RTTM_FOLDER = Path("rttm_new")


def get_lst_from_datapartition(filepath) -> list[str]:
    """Extract list of URIs from RAMC's datapartition file"""

    uris = []
    with open(filepath, "r") as f:
        for line in f:
            if ".wav" in line:
                uri = line.split("\t")[0].strip().replace(".wav", "")
                uris.append(uri)
    return uris


def parse_annotationtxt(filepath):
    timedata_re = re.compile(r"\[(?P<start>\d+\.\d+),(?P<end>\d+\.\d+)\]")

    with open(filepath, "r") as f:
        for line in f:
            splitted = line.split("\t")
            if len(splitted) != 4:
                raise RuntimeError(f"Error: [[{line}]], missing column")
            timedata, label, gender, transcription = splitted
            td_match = timedata_re.match(timedata)
            if not td_match:
                raise RuntimeError(f"Error: [[{line}]], timedata not matching regex")
            start = float(td_match.group("start"))
            end = float(td_match.group("end"))
            yield start, end, label.strip(), gender.strip(), transcription.strip()


def annotationtxt_to_rttm(filepath) -> Annotation:
    """Convert annotations found in TXT folder to RTTM format"""

    filepath = Path(filepath)
    uri = filepath.stem

    # list of speaker names
    speakers = []
    for _, _, label, _, _ in parse_annotationtxt(filepath):
        if label != "G00000000":
            speakers.append(label)
    speakers = list(set(speakers))

    # list of tuples (segment, track, label)
    records = []
    for start, end, label, gender, transcription in parse_annotationtxt(filepath):
        # Fake speaker, for special annotations
        if label == "G00000000":
            # overlap
            if transcription == "[+]":
                if len(speakers) != 2:
                    raise RuntimeError(f"Error: overlap with {len(speakers)} speakers known")
                records.append((Segment(start, end), speakers[0], speakers[0]))
                records.append((Segment(start, end), speakers[1], speakers[1]))
            # laughter, etc
            else:
                continue
        # Regular speaker label
        else:
            records.append((Segment(start, end), label, label))

    return Annotation.from_records(records, uri=uri)


def main():
    # Generate uri list files
    LISTS_FOLDER.mkdir(exist_ok=True, parents=True)
    for partition in PARTITIONS:
        dp_filepath = OG_DATAPARTITIONS_FOLDER / f"{partition}.tsv"
        lst = get_lst_from_datapartition(dp_filepath)
        write_stringlist_to_file(LISTS_FOLDER / f"{partition}.txt", lst, sort=True)

    # Generate RTTMs
    RTTM_FOLDER.mkdir(exist_ok=True, parents=True)
    for annotation in OG_ANNOTATIONS_FOLDER.glob("*.txt"):
        rttm = annotationtxt_to_rttm(annotation)
        with open(RTTM_FOLDER / f"{annotation.stem}.rttm", "w") as f:
            rttm.write_rttm(f)

    pass


if __name__ == "__main__":
    main()
