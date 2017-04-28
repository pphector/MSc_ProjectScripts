#!/bin/bash
set -eu -o pipefail

#Program to automate the creation of finder.pl scripts for subsets found in the same folder

if [ "$#" != 3 ] #Are there less/more than three arguments? 
then 
    echo "Error: you provided an incorrect number of arguments."
    echo "Usage: create_stndln_finder.sh promlistpath outputdirectory lengthofseed"
    exit 1
fi

name=$(basename ${1} .prom.fa)

# Make sure to modify the paths appropriately

echo "BEGIN { unshift @INC, 'PATH/TO/perl/lib/perl5' } 

use Seeder::Finder;  
    my \$finder = Seeder::Finder->new( 
    seed_width    => \"${3}\", 
    strand        => \"revcom\", 
    motif_width   => \"12\", 
    n_motif       => \"10\", 
    hd_index_file => \"PATH/TO/perl/seeder/${3}.index\", 
    seq_file      => \"${1}\", 
    bkgd_file     => \"PATH/TO/perl/seeder/glvz/Stuberosum${3}.bkgd\", 
    out_file      => \"${2}${name}.finder\", 
); 
\$finder->find_motifs;
" >>${2}/${name}_finder.pl

