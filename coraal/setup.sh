#!/bin/bash

echo "Downloading files"
mkdir -p "_download"
wget -c -i coraal_list_2022_05.txt -P _download