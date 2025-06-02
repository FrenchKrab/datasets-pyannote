#!/bin/bash

echo '==== Converting TextGrid to RTTM ===='
textgrid-to-rttm ./Train_Ali_far/textgrid_dir ./rttm/Train_Ali_far/short

textgrid-to-rttm ./Eval_Ali/Eval_Ali_far/textgrid_dir ./rttm/Eval_Ali/Eval_Ali_far/short
textgrid-to-rttm ./Eval_Ali/Eval_Ali_near/textgrid_dir ./rttm/Eval_Ali/Eval_Ali_near/short

textgrid-to-rttm ./Test_Ali/Test_Ali_far/textgrid_dir ./rttm/Test_Ali/Test_Ali_far/short
textgrid-to-rttm ./Test_Ali/Test_Ali_near/textgrid_dir ./rttm/Test_Ali/Test_Ali_near/short

echo '==== Converting RTTM filenames ===='
variant-matching rttm/Train_Ali_far/short Train_Ali_far/audio_dir/ rttm/Train_Ali_far/

variant-matching rttm/Eval_Ali/Eval_Ali_far/short Eval_Ali/Eval_Ali_far/audio_dir/ rttm/Eval_Ali/Eval_Ali_far/
variant-matching rttm/Eval_Ali/Eval_Ali_near/short Eval_Ali/Eval_Ali_near/audio_dir/ rttm/Eval_Ali/Eval_Ali_near/

variant-matching rttm/Test_Ali/Test_Ali_far/short Test_Ali/Test_Ali_far/audio_dir/ rttm/Test_Ali/Test_Ali_far/
variant-matching rttm/Test_Ali/Test_Ali_near/short Test_Ali/Test_Ali_near/audio_dir/ rttm/Test_Ali/Test_Ali_near/

# echo "==== Removing obsolete RTTMs ===="
# rm -rdf rttm/Train_Ali_far/short/
# rm -rdf rttm/Eval_Ali/Eval_Ali_far/short/
# rm -rdf rttm/Eval_Ali/Eval_Ali_near/short/
# rm -rdf rttm/Test_Ali/Test_Ali_far/short/
# rm -rdf rttm/Test_Ali/Test_Ali_near/short/


echo '==== Generating URI files from RTTM ===='
rttm-to-urilist ./rttm/Train_Ali_far/ ./uri/train_far.txt
rttm-to-urilist ./rttm/Eval_Ali/Eval_Ali_far/ ./uri/eval_far.txt
rttm-to-urilist ./rttm/Eval_Ali/Eval_Ali_near/ ./uri/eval_near.txt
rttm-to-urilist ./rttm/Test_Ali/Test_Ali_far/ ./uri/test_far.txt
rttm-to-urilist ./rttm/Test_Ali/Test_Ali_near/ ./uri/test_near.txt

echo '==== Generating UEM files from RTTM ===='
rttm-to-uem --audio-template Train_Ali_far/audio_dir/{uri}.wav rttm/Train_Ali_far/ uem/train_far.uem --end-strategy audio 
rttm-to-uem --audio-template Eval_Ali/Eval_Ali_far/audio_dir/{uri}.wav rttm/Eval_Ali/Eval_Ali_far/ uem/eval_far.uem --end-strategy audio
rttm-to-uem --audio-template Eval_Ali/Eval_Ali_near/audio_dir/{uri}.wav rttm/Eval_Ali/Eval_Ali_near/ uem/eval_near.uem --end-strategy audio
rttm-to-uem --audio-template Test_Ali/Test_Ali_far/audio_dir/{uri}.wav rttm/Test_Ali/Test_Ali_far/ uem/test_far.uem --end-strategy audio
rttm-to-uem --audio-template Test_Ali/Test_Ali_near/audio_dir/{uri}.wav rttm/Test_Ali/Test_Ali_near/ uem/test_near.uem --end-strategy audio