#!/bin/bash

echo "Extracting msdwild_wavs.zip"
unzip msdwild_wavs.zip -d .

echo "Downloading RTTMs"
wget -nc "https://github.com/X-LANCE/MSDWILD/raw/master/rttms/all.rttm"
wget -nc "https://github.com/X-LANCE/MSDWILD/raw/master/rttms/few.train.rttm"
wget -nc "https://github.com/X-LANCE/MSDWILD/raw/master/rttms/few.val.rttm"
wget -nc "https://github.com/X-LANCE/MSDWILD/raw/master/rttms/many.val.rttm"

echo "Generating separate RTTM files ..."
python split_rttm.py

echo "Generating URI index ..."
python generate_uris.py index

echo "Generating UEM files ..."
python generate_uems.py

echo "Generating custom URI lists ..."
python generate_uris.py