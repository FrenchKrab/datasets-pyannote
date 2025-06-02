#!/bin/bash

echo "Downloading ..."
wget -c "https://speech-lab-share-data.oss-cn-shanghai.aliyuncs.com/AliMeeting/openlr/Train_Ali_far.tar.gz"
wget -c "https://speech-lab-share-data.oss-cn-shanghai.aliyuncs.com/AliMeeting/openlr/Eval_Ali.tar.gz"
wget -c "https://speech-lab-share-data.oss-cn-shanghai.aliyuncs.com/AliMeeting/openlr/Test_Ali.tar.gz"

echo "Extracting train"
tar -xf Train_Ali_far.tar.gz
echo "Extracting dev"
tar -xf Eval_Ali.tar.gz
echo "Extracting test"
tar -xf Test_Ali.tar.gz