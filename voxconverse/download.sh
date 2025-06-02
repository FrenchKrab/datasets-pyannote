#!/bin/bash

echo "Downloading RTTMs ..."
wget -c "https://github.com/joonson/voxconverse/archive/refs/heads/master.zip"
unzip master.zip
mv voxconverse-master rttm


echo "Downloading wavs ..."
wget -c "https://www.robots.ox.ac.uk/~vgg/data/voxconverse/data/voxconverse_dev_wav.zip"
wget -c "https://www.robots.ox.ac.uk/~vgg/data/voxconverse/data/voxconverse_test_wav.zip"

echo "Extracting train"
unzip voxconverse_dev_wav.zip
echo "Extracting dev"
unzip voxconverse_test_wav.zip

echo "Moving wavs around"
mkdir wavs/
mv audio/ wavs/dev/
mv voxconverse_test_wav/ wavs/test/

echo "Cleaning up MACOSX folder"
rm -rdf __MACOSX/

echo "Generating URIS and UEMs"
python generate_uris_and_uems.py


# # rm *.zip