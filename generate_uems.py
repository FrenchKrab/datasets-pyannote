UEM_OUT="uems/"
URI_LIST_DIR = "lists/"
RTTM_FOLDER = 'rttm'

import glob
from pathlib import Path

def get_time_data(rttm_file: str) -> float:
    with open(rttm_file, 'r') as f:
        latest_time = 0.0
        for line in f:
            splitted = line.split(' ')
            if (len(splitted) < 4):
                continue
            time_begin = float(splitted[3])
            time_end = float(splitted[4])
            latest_time = max(latest_time, time_begin + time_end)
    return latest_time

def generate_uems_for_uris(uris: list, rttm_path: str, out_path: str):
    for uri in uris:
        rttm_file = f"{uri}.rttm"
        earliest_time = 0.0
        latest_time = get_time_data(Path(rttm_path) / rttm_file)

        file_to_write_path = Path(out_path)/f'{uri}.uem'
        file_to_write_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_to_write_path, 'w') as f:
            f.write(f'{uri} 1 {earliest_time} {latest_time}\n')

def read_uris(urifile_path: str):
    uris = []
    with open(urifile_path, 'r') as f:
        for l in f:
            uris.append(l.replace('\n',''))
    return uris


def main():
    list_path = Path(URI_LIST_DIR)

    for filename in glob.glob(URI_LIST_DIR + "/*"):
        subsetname = Path(filename).stem

        subset_uris = read_uris(filename)
        generate_uems_for_uris(subset_uris, Path(RTTM_FOLDER), UEM_OUT)


if __name__ == "__main__":
    main()