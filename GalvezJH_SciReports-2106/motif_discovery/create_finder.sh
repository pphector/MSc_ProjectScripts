#!/bin/bash
set -eu -o pipefail

#Program to automate the creation of finder.pl scripts for subsets found in the same folder

if [ "$#" != 2 ] #Are there less/more than two arguments? 
then 
    echo "Error: you provided an incorrect number of arguments." 
    echo "Usage: create_finder.sh directorypath lengthofseed"
    exit 1
fi

mkdir ${1}/finders ${1}/motifs

# Make sure to modify paths appropriately

for i in $(ls -v ${1}/*fas)
do

    name=$(basename $i .fas)

    touch ${1}/finders/${name}_finder.pl

    echo "BEGIN { unshift @INC, 'PATH/TO/perl/lib/perl5' } 

use Seeder::Finder;  
    my \$finder = Seeder::Finder->new( 
    seed_width    => \"${2}\", 
    strand        => \"revcom\", 
    motif_width   => \"12\", 
    n_motif       => \"10\", 
    hd_index_file => \"PATH/TO/perl/seeder/${2}.index\", 
    seq_file      => \"${i}\", 
    bkgd_file     => \"PATH/TO/perl/seeder/glvz/Stuberosum${2}.bkgd\", 
    out_file      => \"${1}/motifs/$(basename ${i} .fas).finder\", 
); 
\$finder->find_motifs;
" >> ${1}/finders/${name}_finder.pl

done

