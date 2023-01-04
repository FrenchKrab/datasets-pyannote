
from pathlib import Path
from typing import List, Literal, Text, Union

from .audio import get_time_data_from_wav
from .rttm import get_time_data_from_rttm


def generate_uems_for_uris(rttm_folder: Union[Text, Path], out_folder: Union[Text, Path], uris: List[Text], audio_path_template:str=None, audio_use: Literal['everything','safeguard','nothing']='safeguard'):
    """Given a list of URIs and an RTTM folder, generate the corresponding UEM for each URI.
    Can use audio files for RTTM start/end time sanity check

    Parameters
    ----------
    rttm_folder : Union[Text, Path]
        Folder with RTTM files named {uri}.rttm
    out_folder : Union[Text, Path]
        Output folder for .uem files
    uris : List[Text]
        List of URIs
    audio_path_template : str, optional
        Path where to find the audio files. eg 'wav/{uri}.wav'
        Don't use audio file to compute UEM if left to None, by default None
    audio_use : Literal['everything','safeguard','nothing'], optional
        How to make use of audio files for UEM
        'everything'=ignore RTTMs and only use audio files, 
        'safeguard'=prefer rttm but make sure the timestamps are sane, 
        'nothing'=dont use audio files, 
        by default 'safeguard'
    """

    # TODO: add option for how to handle starting time.
    for uri in uris:
        rttm_file = f"{uri}.rttm"
        rttm_path = Path(rttm_folder) / rttm_file
        wav_path = Path(eval(f'f"{audio_path_template}"')) if audio_path_template is not None else None

        earliest_time = 0.0

        rttm_duration = get_time_data_from_rttm(rttm_path)['latest_time']
        latest_time = rttm_duration
        
        # use the audio file if possible and desired
        if wav_path is not None and wav_path.exists():
            wav_duration = get_time_data_from_wav(wav_path)
            if audio_use == 'everything':
                latest_time = wav_duration
            elif audio_use == 'safeguard':
                latest_time = min(rttm_duration, wav_duration)

        file_to_write_path = Path(out_folder)/f'{uri}.uem'
        file_to_write_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_to_write_path, 'w') as f:
            f.write(f'{uri} 1 {earliest_time} {latest_time}\n')
