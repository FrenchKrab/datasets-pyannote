### LINK THE DATA
mkdir -p data
ln -s /somewhere/third_dihard_challenge_dev/data/ data/dev
ln -s /somewhere/third_dihard_challenge_eval/data/ data/eval


### CREATE LISTS OF AVAILABLE FILES
mkdir -p lists/raw/dev

for set in dev eval
do
    rm -rf lists/raw/$set
    mkdir -p lists/raw/$set
    for f in data/$set/uem_scoring/full/*.uem
    do
        domain=$(basename $f .uem)
        cat $f | cut -d " " -f 1 > lists/raw/$set.$domain.txt
        sort -u lists/raw/$set.$domain.txt -o lists/raw/$set.$domain.txt
    done
done

### CREATE CUSTOM SUBSETS FOR TRAIN/VAL
rm -rf lists/custom1
for subset_uris in lists/raw/dev.*.txt
do
    # if subset contains 'all', continue
    if [[ $subset_uris == *"all"* ]]; then
        continue
    fi
    subset_name=`basename $subset_uris .txt | cut -d "." -f 2`

    uri-subsets time ratio lists/raw/dev.${subset_name}.txt --subsets validation.${subset_name} 0.25 train.${subset_name} -1 --output lists/custom1/ --uem data/dev/uem/{uri}.uem --verbose
done
cat lists/custom1/train.*.txt > lists/custom1/train.all.txt
cat lists/custom1/validation.*.txt > lists/custom1/validation.all.txt