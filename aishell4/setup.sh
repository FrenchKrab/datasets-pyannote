#!/bin/bash


echo "Downloading ..."
wget c "https://www.openslr.org/resources/111/train_L.tar.gz"
wget -c "https://www.openslr.org/resources/111/train_M.tar.gz"
wget -c "https://www.openslr.org/resources/111/train_S.tar.gz"
wget -c "https://www.openslr.org/resources/111/test.tar.gz"

echo "Extracting train_L"
tar -xf train_L.tar.gz
echo "Extracting train_M"
tar -xf train_M.tar.gz
echo "Extracting train_S"
tar -xf train_S.tar.gz
echo "Extracting test"
tar -xf test.tar.gz

echo "Bringing every training data in the same folders ..."
mkdir wav
mkdir rttm

mv train_L/wav/* wav/
mv train_L/TextGrid/* rttm/
rm -rd train_L/

mv train_M/wav/* wav/
mv train_M/TextGrid/* rttm/
rm -rd train_M/

mv train_S/wav/* wav/
mv train_S/TextGrid/* rttm/
rm -rd train_S/

mv test/wav/* wav/
mv test/TextGrid/* rttm/
rm -rd test/


echo "Generating URI index ..."
python generate_uris.py index

echo "Generating UEM files ..."
python generate_uems.py

echo "Generating URI lists ..."
python generate_uris.py

echo "Done !"
