MONOLITHIC_RTTM_PATH = "all.rttm"
OUT_FOLDER = "rttm"

import os
from pathlib import Path

def split_monolithic(monolithic_path: str, out_path: str):
    Path(out_path).mkdir(parents=True, exist_ok=True)
    with open(monolithic_path, 'r') as f:
        for line in f:
            splitted = line.split(' ')
            file_name = splitted[1]
            with open(os.path.join(out_path, f"{file_name}.rttm"), 'a+') as f2:
                f2.write(line)



def main():
    split_monolithic(MONOLITHIC_RTTM_PATH, OUT_FOLDER)    
    pass

if __name__ == "__main__":
    main()