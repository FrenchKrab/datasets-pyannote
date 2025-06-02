import glob
from pathlib import Path
from typing import List, Optional, Text


def write_stringlist_to_file(filepath: str | Path, stringlist: List[Text], sort: bool = False):
    if sort:
        stringlist.sort()
    file_to_write_path = Path(filepath)
    file_to_write_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_to_write_path, "w") as f:
        for s in stringlist:
            f.write(s + "\n")


def read_stringlist_from_file(filepath: str) -> List[Text]:
    stringlist = []
    with open(filepath, "r") as f:
        for l in f:
            stringlist.append(l.replace("\n", ""))
    return stringlist


def get_files_in_paths(paths: List[str], glob_pattern: Optional[str] = None) -> List[Path]:
    result: List[Path] = []
    for p_str in paths:
        p = Path(str(p_str))
        if p.is_dir():
            if glob_pattern is None:
                result.extend([f for f in p.glob("*") if f.is_file()])
            else:
                result.extend([f for f in p.glob(glob_pattern) if f.is_file()])
        else:
            result.append(p)
    return result
