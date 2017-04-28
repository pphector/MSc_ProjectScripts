#!/bin/bash
set -eu -o pipefail

if [ "$#" != 2 ] #Are there less/more than two arguments? 
then 
    echo "Error: you provided an incorrect number of arguments. "
    echo "Usage: getpromloc.sh promoterlist allpromoterlist"
    exit 1
fi 

#THIS SCRIPT REQUIRES A TEXT FILE WITH ALL GENE NAMES AND PROMOTER COORDINATES
#This file can now be easily generated using the sqlite3 db for the ITAG1 annotation

#Create the name of the results file
results=($(basename "$1" _acc.txt).prom.fa)

#Create a bash array with all unique gene names in the list
gene_names=($(grep "^Sotub" "$1")) 
#echo ${gene_names[*]}

for gene in ${gene_names[*]} #For every gene in the gene_names array
do 
   #Get the promoter location from the allpromoterlist
   promloc=$(grep "${gene}" ${2} | cut --fields 1)

   samtools faidx $GENOME/Stuberosum_genome.ITAG1.fa ${promloc} >>$results
done
 
