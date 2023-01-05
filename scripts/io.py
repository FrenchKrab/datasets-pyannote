import glob
from pathlib import Path
from typing import List, Text


def write_stringlist_to_file(filepath: str, stringlist: List[Text], sort: bool=False):
    if sort:
        stringlist.sort()
    file_to_write_path = Path(filepath)
    file_to_write_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_to_write_path, 'w') as f:
        for s in stringlist:
            f.write(s+"\n")


def read_stringlist_from_file(filepath: str) -> List[Text]:
    stringlist = []
    with open(filepath, 'r') as f:
        for l in f:
            stringlist.append(l.replace('\n',''))
    return stringlist