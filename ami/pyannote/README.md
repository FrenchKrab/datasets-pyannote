# How to use in `pyannote`

## Download AMI corpus

This will download the AMI corpus MixHeadset files into `AMI-diarization-setup/pyannote/amicorpus`:

```bash
cd AMI-diarization-setup/pyannote
sh download_ami.sh
```

## Use AMI diarization setup proposed by BUT

```python
# tell pyannote.database where to find partition, reference, and wav files
import os
os.environ["PYANNOTE_DATABASE_CONFIG"] = 'AMI-diarization-setup/pyannote/database.yml'

# used to automatically find paths to wav files
from pyannote.database import FileFinder
preprocessors = {'audio': FileFinder()}

# initialize 'only_words' experimental protocol
from pyannote.database import get_protocol
only_words = get_protocol('AMI.SpeakerDiarization.only_words', preprocessors=preprocessors)

# iterate over the training set
for file in only_words.train():
    meeting = file['uri']
    reference = file['annotation']
    path = file['audio']

# iterate over the development set
for file in only_words.development():
    pass

# iterate over the test set
for file in only_words.test():
    pass

# initialize 'word_and_vocalsounds' experimental protocol
word_and_vocalsounds = get_protocol('AMI.SpeakerDiarization.word_and_vocalsounds')
```
