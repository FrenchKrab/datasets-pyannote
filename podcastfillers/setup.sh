#!/bni/bash

echo "Downloading ..."
wget -c https://zenodo.org/record/7121457/files/PodcastFillers.zip?download=1 -O PodcastFillers.zip
wget -c https://zenodo.org/record/7121457/files/PodcastFillers.z01?download=1 -O PodcastFillers.z01
wget -c https://zenodo.org/record/7121457/files/PodcastFillers.z02?download=1 -O PodcastFillers.z02
wget -c https://zenodo.org/record/7121457/files/PodcastFillers.z03?download=1 -O PodcastFillers.z03

echo "Extracting ..."
unzip PodcastFillers.zip

echo "Generatig URI lists ..."

SRC_DIR=PodcastFillers
# change this if PodcastFillers has been downloaded and extracted elsewhere
# SRC_DIR=/gpfsdswork/dataset/PodcastFillers

TGT_DIR=/gpfswork/rech/eie/commun/data/PodcastFillers

SYMLINK_DIR=$TGT_DIR/symlinks
mkdir -p $SYMLINK_DIR

OLD_IFS="$IFS"
IFS=$'\n'

for SUBSET in test train validation; do

    # delete list of uris if it exists
    if [ -f $TGT_DIR/$SUBSET.uris.lst ]; then
        rm $TGT_DIR/$SUBSET.uris.lst
    fi

    for file in `find $SRC_DIR/audio/episode_wav/$SUBSET -name "*wav" -type f`; do

        # build "uri" by removing extension and replacing spaces with underscores        
        base=`basename "$file"`
        stem=`echo $base | sed 's/\.[^.]*$//'`
        URI=`echo $stem | tr ' ' '_'`

        # add "uri" to list of uris
        echo $URI >> $TGT_DIR/$SUBSET.uris.lst 

        # create symlink
        ln -s "$file" "$SYMLINK_DIR/$URI.wav"
    done
    
done

IFS="$OLD_IFS"

echo "Generating UEMs and RTTMs..."
python generate.py $SRC_DIR $TGT_DIR



