import wave
import contextlib
import sys
import csv

src_dir = sys.argv[1]
tgt_dir = sys.argv[2]

SUBSET = {"train": "train", "development": "validation", "test": "test"}


for subset, slug in SUBSET.items():

    with open(f"{tgt_dir}/{slug}.uris.lst", "r") as f:
        uris = [line.strip() for line in f.readlines()]

    with open(f"{tgt_dir}/{subset}.uem", "w") as f:
        for uri in uris:
            filename = f"{tgt_dir}/symlinks/{uri}.wav"
            with contextlib.closing(wave.open(filename,'r')) as g:
                frames = g.getnframes()
                rate = g.getframerate()
                duration = frames / float(rate)
                f.write(f"{uri} 1 0.000 {duration:.3f}\n")

with open(f'{src_dir}/PodcastFillers.csv', 'r') as csvfile, open(f'{tgt_dir}/full.rttm', 'w') as rttm_full, open(f'{tgt_dir}/consolidated.rttm', 'w') as rttm_consolidated:
    csvreader = csv.reader(csvfile, delimiter=',')
    for r, row in enumerate(csvreader):
        
        if r == 0:
            continue
        
        _, _, label_full_vocab, label_consolidated_vocab, filename, start_time, end_time, *_ = row
        uri = filename.replace(' ', '_')
        start_time = float(start_time)
        end_time = float(end_time)

        rttm_full.write(f"SPEAKER {uri} 1 {start_time:.3f} {end_time - start_time:.3f} <NA> <NA> {label_full_vocab} <NA> <NA>\n")

        if label_consolidated_vocab == 'None':
            continue

        rttm_consolidated.write(f"SPEAKER {uri} 1 {start_time:.3f} {end_time - start_time:.3f} <NA> <NA> {label_consolidated_vocab} <NA> <NA>\n")
