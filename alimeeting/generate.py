from lhotse import RecordingSet, SupervisionSet
from pyannote.core import Annotation, Timeline, Segment
from pyannote.audio import Audio
from tqdm import tqdm
from pathlib import Path

get_duration = Audio().get_duration


subsets = {'train': 'train', 'development': 'eval', 'test': 'test'}


if __name__ == '__main__':
    for subset, slug in subsets.items():
        recordings = RecordingSet.from_file(f"alimeeting-sdm_recordings_{slug}.jsonl.gz")
        uris = dict()
        with open(f"{subset}.uri.lst", "w") as lst, open(f"{subset}.uem", "w") as uem, open(f"channel.{subset}.map", "w") as cnl:
            for recording in recordings:
                uri = Path(recording.sources[0].source).stem
                uris[recording.id] = uri
                lst.write(f"{uri}\n")
                cnl.write(f"{uri} 1\n")
                duration = get_duration(recording.sources[0].source)
                annotated = Timeline([Segment(0.0, duration)], uri=uri)
                annotated.write_uem(uem)

        supervisions = SupervisionSet.from_file(f"alimeeting-sdm_supervisions_{slug}.jsonl.gz")
        annotations = dict()
        for s, supervision in tqdm(enumerate(list(supervisions)), desc=subset):
            uri = uris[supervision.recording_id]
            segment = Segment(supervision.start, supervision.start + supervision.duration)
            channel = supervision.channel
            assert channel == 0
            speaker = supervision.speaker
            if uri not in annotations:
                annotations[uri] = Annotation(uri=uri)
            annotations[uri][segment, s] = speaker

        with open(f"{subset}.rttm", "w") as rttm:
            for uri, annotation in annotations.items():
                annotation.write_rttm(rttm)
