
import contextlib
import wave


def get_time_data_from_wav(wav_file: str) -> float:
    with contextlib.closing(wave.open(str(wav_file),'r')) as f: 
        frames = f.getnframes()
        rate = f.getframerate()
        length = frames / float(rate)    
        return length