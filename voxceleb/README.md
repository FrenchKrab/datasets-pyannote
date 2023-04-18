# VoxCeleb for pyannote.audio

## Usage

```python
from pyannote.database import registry
registry.load_database("database.yml")

protocol = registry.get_protocol("VoxCeleb.SpeakerVerification.VoxCeleb")

# iterate on all VoxCeleb1 dev (but speakers whose names starts with U, V, or W) and on all VoxCeleb2 dev
for file in protocol.train():
    pass

# iterate on all VoxCeleb1 dev speakers whoe names starts with U, V, or W
for file in protocol.development():
    pass

# iterate over target/non-target trials between the above UVW speakers
for trial in protocol.development_trial():
    pass

# iterate over target/non-target trials defined VoxCeleb1 "original"
for trial in protocol.test_trial():
    pass
```


