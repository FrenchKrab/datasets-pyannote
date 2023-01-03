# echo "Extracting msdwild_wavs.zip"
# unzip msdwild_wavs.zip -d .

echo "Downloading RTTMs"
wget -nc "https://github.com/X-LANCE/MSDWILD/raw/master/rttms/all.rttm"
wget -nc "https://github.com/X-LANCE/MSDWILD/raw/master/rttms/few.train.rttm"
wget -nc "https://github.com/X-LANCE/MSDWILD/raw/master/rttms/few.val.rttm"
wget -nc "https://github.com/X-LANCE/MSDWILD/raw/master/rttms/many.val.rttm"

python split_rttm.py
python generate_uris.py
python generate_uems.py