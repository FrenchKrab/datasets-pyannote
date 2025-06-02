from logging import warn
from pathlib import Path
from typing import List, Literal, Optional, Text, Union

from pyannote.core import Annotation
from pyannote.database.util import load_rttm

from .audio import get_time_data_from_wav
from .rttm import get_time_data_from_rttm


def generate_uems_for_uris(
    rttm_folder: Union[Text, Path],
    out_folder: Union[Text, Path],
    uris: List[Text],
    audio_path_template: str = None,
    audio_use: Literal["everything", "safeguard", "nothing"] = "safeguard",
):
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

        rttm_duration = get_time_data_from_rttm(rttm_path)["latest_time"]
        latest_time = rttm_duration

        # use the audio file if possible and desired
        if wav_path is not None and wav_path.exists():
            wav_duration = get_time_data_from_wav(wav_path)
            if audio_use == "everything":
                latest_time = wav_duration
            elif audio_use == "safeguard":
                latest_time = min(rttm_duration, wav_duration)

        file_to_write_path = Path(out_folder) / f"{uri}.uem"
        file_to_write_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_to_write_path, "w") as f:
            f.write(f"{uri} 1 {earliest_time} {latest_time}\n")


def generate_uems_for_uris_v2(
    rttms: List[Path] | dict[str, Annotation],
    out_path: str,
    start_strategy: Literal["rttm", "zero"] = "zero",
    end_strategy: Optional[Literal["audio", "rttm_safe", "rttm"]] = None,
    audio_path_template: Optional[str] = None,
):
    """Generate UEM files from a list of RTTM files (and optionally audio files).

    Parameters
    ----------
    rttms : List[Path]
        Path to the rttm files
    out_path : str
        Path to the output(s). Will generate one file per URI if the name contains `{uri}`.
    start_strategy : Literal[&#39;rttm&#39;, &#39;zero&#39;], optional
        How to determine the UEM start time.
        - `zero` always sets it to 0.0
        - `rttm` sets it at the start of the earliest RTTM segment, by default 'zero'

    end_strategy : Optional[Literal[&quot;audio&quot;, &quot;rttm_safe&quot;, &quot;rttm&quot;]], optional
        How to choose the UEM end time.

        - `audio`: determined from audio
        - `rttm_safe`: determined from RTTM but clipped to audio duration if it exceeds it
        - `rttm`: determined from RTTM only

        If left to None, will default to rttm_safe if audio is available, else will fall back on rttm.
        By default None
    audio_path_template : Optional[str], optional
        Path template to the audio files. e.g `wavs/{uri}.wav;wavs/{uri}.flac`, by default None
    """
    # Initialize
    audio_path_templates = audio_path_template.split(";") if audio_path_template is not None else []

    if end_strategy is None:
        end_strategy = "rttm_safe" if len(audio_path_templates) > 0 else "rttm"

    # Load all RTTMs if needed
    if isinstance(rttms, list):
        rttms_dict: dict[str, Annotation] = {}
        for rttm_path in rttms:
            rttms_dict.update(load_rttm(rttm_path))
        rttms = rttms_dict

    # Find start/end
    for i, uri in enumerate(rttms.keys()):
        rttm_extent = rttms[uri].get_timeline().extent()

        if start_strategy == "zero":
            earliest_time = 0.0
        else:
            earliest_time = rttm_extent.start
        latest_time = rttm_extent.end

        # use the audio file if desired
        if end_strategy in ["audio", "rttm_safe"]:
            wav_path: Optional[Path] = None
            for template in audio_path_templates:
                path = Path(eval(f'f"{audio_path_template}"'))
                if path.exists():
                    wav_path = path
                    break

            # use the audio file if possible
            if wav_path is not None:
                wav_duration = get_time_data_from_wav(wav_path)
                if end_strategy == "audio":
                    latest_time = wav_duration
                elif end_strategy == "rttm_safe":
                    latest_time = min(latest_time, wav_duration)
            else:
                warn(f"Audio file not found for {uri}, falling back on RTTM for UEM end time")

        out_path = str(out_path)
        if "{uri}" in out_path:
            file_to_write_path = Path(out_path.format(uri=uri))
            file_to_write_path.unlink(missing_ok=True)
        else:
            file_to_write_path = Path(out_path)
            if i == 0:
                file_to_write_path.unlink(missing_ok=True)
        file_to_write_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_to_write_path, "a") as f:
            f.write(f"{uri} 1 {earliest_time} {latest_time}\n")


def get_uem_data(path: Union[str, Path]) -> dict:
    with open(path, "r") as f:
        line = f.readline().strip()
        line_data = line.split(" ")
        if len(line_data) != 4:
            raise Exception(f"Invalid UEM file, contains only {len(line_data)} fields")

        return {
            "uri": line_data[0],
            "track": line_data[1],
            "time_start": float(line_data[2]),
            "time_end": float(line_data[3]),
        }


def get_uem_data_uris(uris: List[Text], uem_template: str):
    # compute file durations / total durations
    files_duration: dict[str, float] = {}
    total_time = 0.0

    for uri in uris:
        uem_data = get_uem_data(eval(f'f"{uem_template}"'))
        files_duration[uri] = uem_data["time_end"] - uem_data["time_start"]
        total_time += files_duration[uri]
    return files_duration, total_time
