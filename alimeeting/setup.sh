#!/bin/bash

echo "Downloading and extracting ..."
lhotse download ali-meeting .

echo "Preparing ..."
lhotse prepare ali-meeting --mic sdm --save-mono . .

echo "Generating URI lists and UEM files ..."
python generate.py

echo "Done !"
