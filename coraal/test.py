
from cgitb import text
import math
import re

KEEP_ALL_NON_LINGUISTICS=[
    "cough", "clears throat", "laugh", "yawns", "snap", "sound effect", "grumbles",
    "inhale", "exhale", "microphone feedback", "clap", "ts", "pp", "imitates music"
]

def txt_to_rttm(in_file:str, out_file:str, stitch_nonspeech_threshold:float=0.0, keep_non_linguistics:list=[]):
    """Convert a CORAAL text file into an RTTM file.

    Parameters
    ----------
    in_file : str
        Input CORAAL text file
    out_file : str
        Output RTTM to write to
    stitch_nonspeech_threshold : float, optional
        CORAAL transcripts have pauses annotated, aswell as certain
        non lingual annotations.
        Under which threshold (in seconds) should these 'pauses' be
        considered as speech ?, by default 0.0
    keep_non_linguistics : list, optional
        List of non linguistic annotation to consider
        as speech when it's the sole thing in the annotation
        see KEEP_ALL_NON_LINGUISTICS or the CORAAL user guide
        for a list. Defaults to considering all of them 
        as nonspeech, by default []
    """

    with open(in_file, 'r') as f:
        f.readline()    # discard first line (header)
        with open(out_file, 'w') as f2:
            for l in f.readlines():
                l = l.strip()
                line, speaker_id, tbeg, content, tend = l.split("\t")
                text_content = re.sub(r"[^a-zA-Z<> ]+", "", content)    # helps remove [] and punctuations
                duration = round(float(tend)-float(tbeg), 6)

                # Check if line is non-speech
                is_not_speech = False
                if content.startswith("(pause "):
                    is_not_speech = True
                elif (  
                        text_content.startswith("<") and text_content.endswith(">") and 
                        text_content.count("<") == 1 and text_content.count(">") == 1 and 
                        text_content not in keep_non_linguistics
                    ):
                    is_not_speech = True
                
                # If this line is not speech and is too long to be considered stitch candidate, ignore it (= silence)
                if is_not_speech and duration > stitch_nonspeech_threshold:
                    continue

                # write the RTTM line
                l_rttm = f"SPEAKER {in_file} 1 {tbeg} {duration} <NA> <NA> {speaker_id}\n"
                f2.write(l_rttm)

# SPEAKER 20200616_M_R001S01C01 1 5.4102 3.3100 <NA> <NA> 001-M <NA> <NA>
# SPEAKER file chnl tbeg tdur <NA> <NA> name <NA> <NA>

txt_to_rttm("ATL_se0_ag1_f_01_1.txt", "TEST.rttm", 0)