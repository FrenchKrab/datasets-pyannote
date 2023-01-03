import contextlib
from typing import Literal
import wave


UEM_OUT="uems/"
URI_LIST_DIR = "lists/"
WAV_FOLDER="wav"
WAV_EXTENSION=".wav"
RTTM_FOLDER = 'rttm'

# none: dont use wavs
# safeguard: use wav duration to clip rttm if an annotation exceed file duration
# everything: use wave duration as uem
WAV_USE: Literal['none','safeguard','everything'] = 'safeguard'



import glob
from pathlib import Path

def get_time_data_from_rttm(rttm_file: str) -> float:
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

def get_time_data_from_wav(wav_file: str) -> float:
    with contextlib.closing(wave.open(str(wav_file),'r')) as f: 
        frames = f.getnframes()
        rate = f.getframerate()
        length = frames / float(rate)    
        return length


def generate_uems_for_uris(uris: list):
    for uri in uris:
        rttm_file = f"{uri}.rttm"
        rttm_path = Path(RTTM_FOLDER) / rttm_file
        wav_file = f"{uri}{WAV_EXTENSION}"
        wav_path = Path(WAV_FOLDER) / wav_file


        earliest_time = 0.0

        rttm_duration = get_time_data_from_rttm(rttm_path)
        wav_duration = get_time_data_from_wav(wav_path)
        if WAV_USE == 'everything':
            latest_time = wav_duration
        elif WAV_USE == 'safeguard':
            latest_time = min(rttm_duration, wav_duration)
        else:
            latest_time = rttm_duration

        file_to_write_path = Path(UEM_OUT)/f'{uri}.uem'
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
    for filename in glob.glob(URI_LIST_DIR + "/*"):
        subsetname = Path(filename).stem

        subset_uris = read_uris(filename)
        generate_uems_for_uris(subset_uris)


if __name__ == "__main__":
    main()