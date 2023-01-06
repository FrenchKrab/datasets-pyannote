#!/bin/bash

echo "Downloading arabic-speech-corpus.zip ..."
wget -c http://en.arabicspeechcorpus.com/arabic-speech-corpus.zip


echo "Extracting arabic-speech-corpus.zip"
unzip arabic-speech-corpus.zip -d .


echo "Moving folders around ..."
mv arabic-speech-corpus/* ./
rm -d arabic-speech-corpus/
mv "test set" test_set


echo "Renaming files ..."
function extract_id {
    # Files all have names like >ARA NORM  0001.wav<, get 0001.wav
    echo $1 | grep -Po '[0-9]+\..*'
}
function rename_all {
    local prefix=$1
    local folder=$2
    local pattern=$3
    for f in ${folder}/${pattern}*
    do
        id=`extract_id "$f"`
        mv "$f" "${folder}/${prefix}${id}"
    done
}
rename_all TRAIN_ wav ARA
rename_all TRAIN_ textgrid ARA
rename_all TRAIN_ lab ARA
rename_all TEST_ "test_set/wav" ARA
rename_all TEST_ "test_set/textgrid" ARA
rename_all TEST_ "test_set/lab" ARA