#!/bin/bash
set -eu -o pipefail

if [ "$#" != 2 ] #Are there less/more than two arguments? 
then 
    echo "Error: you provided an incorrect number of arguments. "
    echo "Usage: getaccessions.sh filenamepath IDColumn"
    exit 1
fi

#Specify input samples file where the first column is the name of each gene list. 
#Create a Bash array from the first column of the files listed in the input sample file

genelists=($(grep -v "^#" "$1" | cut -f 1 ))

for list in ${genelists[*]}
do 
  #Create accession list with only accession numbers
  accession_file="$(basename $list .txt)_acc.txt"

  #Obtain only the ITAG accession numbers based on the column specified by user
  cut -f ${2} "$list" > ./$accession_file

done