#!/bin/bash



echo "Downloading ..."
wget -c https://zenodo.org/record/7121457/files/PodcastFillers.zip?download=1 -O PodcastFillers.zip
wget -c https://zenodo.org/record/7121457/files/PodcastFillers.z01?download=1 -O PodcastFillers.z01
wget -c https://zenodo.org/record/7121457/files/PodcastFillers.z02?download=1 -O PodcastFillers.z02
wget -c https://zenodo.org/record/7121457/files/PodcastFillers.z03?download=1 -O PodcastFillers.z03
wget -c https://zenodo.org/record/7121457/files/PodcastFillers.csv?download=1 -O PodcastFillers.csv

echo "Extracting ..."
unzip PodcastFillers.zip

echo "Generatig URI lists ..."

SYMLINK_DIR=$PWD/symlinks
mkdir -p $SYMLINK_DIR

OLD_IFS="$IFS"
IFS=$'\n'

for SUBSET in test train validation; do

    # delete list of uris if it exists
    if [ -f $PWD/$SUBSET.uris.lst ]; then
        rm $PWD/$SUBSET.uris.lst
    fi

    # FIXME: this is probably not the right relative path to PodcastFillers
    for file in `find $PWD/PodcastFillers/audio/episode_wav/$SUBSET -name "*wav" -type f`; do

        # build "uri" by removing extension and replacing spaces with underscores        
        base=`basename "$file"`
        stem=`echo $base | sed 's/\.[^.]*$//'`
        URI=`echo $stem | tr ' ' '_'`

        # add "uri" to list of uris
        echo $URI >> $PWD/$SUBSET.uris.lst 

        # create symlink
        ln -s "$file" "$SYMLINK_DIR/$URI.wav"
    done
    
done

IFS="$OLD_IFS"

echo "Generating UEMs and RTTMs..."
python generate.py $PWD
