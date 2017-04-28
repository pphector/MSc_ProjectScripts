#!/bin/bash
set -eu -o pipefail

#Program to automate the creation of subsets for promoters lists with more than x promoters
#Uses pmunusamy's subset creation python script

if [ "$#" != 3 ] #Are there less/more than two arguments? 
then 
    echo "Error: you provided an incorrect number of arguments." 
    echo "Usage: ./make_subsets.sh filepath maxnumofpromoters numofsubgroups "
    exit 1
fi

for i in $(ls $1 | grep .prom.fa) #For all promoter lists in the specified direcory (first argument)
do
    echo $i
    number=$(grep "^>" $1/$i | wc -l)
    if [ $number -gt $2 ] #If there are more promoters in the list than there should be (for seeder)
    then
        echo $number "Is bigger than the max allowed, creating subsets"
        mkdir $1/$(basename $i .prom.fa)
        cd $1/$(basename $i .prom.fa)
        #Execute the actual python script. Modification was made so that it includes a second argument specifying number of subgroups.
        # If python script is not in this directory, add appropriate path. 
        python ./random_sampling.py $1/$i $3 $(basename $i .prom.fa)
    fi
done
