import contextlib
import wave
from pathlib import Path
from typing import Union

import torchaudio


def get_time_data_from_wav(wav_file: Union[str, Path]) -> float:
    metadata = torchaudio.info(wav_file)
    return 1.0 * metadata.num_frames / metadata.sample_rate

    # with contextlib.closing(wave.open(str(wav_file),'r')) as f:
    #     frames = f.getnframes()
    #     rate = f.getframerate()
    #     length = frames / float(rate)
    #     return length
