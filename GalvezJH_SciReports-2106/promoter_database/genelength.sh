#!/bin/bash
#Exit immediately on error
set -eu -o pipefail

if [ "$#" != 1 ] #Are there less/more than two arguments? 
then 
    echo "Error: you provided an incorrect number of arguments."
    echo "Usage: genelength.sh genelistfile"  
    exit 1
fi 

#Create the name of the results file
results=$(basename "$1" .tsv)_length.tsv
#echo $results

#Create a bash array with all unique gene names in the list
gene_names=$(cut --fields 1 ${1}) 

for gene in ${gene_names[*]} #For every gene in the gene_names array
do 
   #Get the gene start position 
   gene_start=$(grep --max-count=1 "${gene}" ${1} |\
      cut --fields 2)
   #Get the gene end position
   gene_end=$(grep --max-count=1 "${gene}" ${1} |\
      cut --fields 3)
   #Calculate gene length
#   echo ${gene_start}, ${gene_end}
   let gene_length="${gene_end}-${gene_start}"
   #Write the result in the results file
   echo -e "${gene}\t${gene_length}" >>$results
done

