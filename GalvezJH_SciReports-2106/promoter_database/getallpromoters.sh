#!/bin/bash
set -eu -o pipefail

if [ "$#" != 1 ] #Are there less/more than one arguments? 
then 
    echo "Error: you provided an incorrect number of arguments. "
    echo "Usage: getallpromoters.sh allpromoterlist.loc"
    exit 1
fi 

#THIS SCRIPT REQUIRES A TEXT FILE WITH ALL GENE NAMES AND PROMOTER COORDINATES
#This file can now be easily generated using the sqlite3 db for the ITAG1 annotation 
#This program assumes that the file ends with .loc

#Create the name of the results file
results=$(basename $1 .loc).fa

for line in ${1}  #For every line in the inputfile
do 
    #Get the promoter locations from the allpromoterlist
    promloc=$(cut --fields 1 ${line})

    #echo ${promloc}
    
    samtools faidx $GENOME/Stuberosum_genome.ITAG1.fa ${promloc} >>$results 
done


