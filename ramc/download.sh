# echo "Downloading the dataset"
# wget -c https://www.openslr.org/resources/123/MagicData-RAMC.tar.gz


echo "Extracting dataset"
tar -xf MagicData-RAMC.tar.gz

echo "Preparing URIs and RTTMs"
python prepare_uri_rttm.py

echo "Preparing UEMs"
rttm-to-uem rttm/* uem/all.uem --audio-template MDT2021S003/WAV/{uri}.wav --end-strategy audio


# uri-subsets time absolute lists/dev.txt --output lists/dev2h/ --uem uem/all.uem --subsets 2h 7200