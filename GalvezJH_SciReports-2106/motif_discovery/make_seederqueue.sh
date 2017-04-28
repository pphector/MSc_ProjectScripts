#!/bin/bash
set -eu -o pipefail 

if [ "$#" != 3 ] #Are there less/more than three arguments? 
then
    echo "Error: you provided an incorrect number of arguments."
    echo "Usage: make_seederqueue.sh directorypath outputname timeinhours"
    exit 1
fi

# Substitute appropriate project name (for Compute Canada) and email address

echo "#!/bin/bash
#PBS -A prj-id-No
#PBS -l walltime=${3}:00:00
#PBS -l nodes=1:ppn=4
#PBS -q xlm2
#PBS -m bea
#PBS -M email@address.ca
#PBS -r n
set -eu -o pipefail

">> ${2}

subsetlist=$(ls -v ${1})
for i in ${subsetlist}
do
    echo "perl ${1}/${i}" >>${2}
done


