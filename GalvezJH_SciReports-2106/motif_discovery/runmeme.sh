#!/bin/bash
set -eu -o pipefail 

if [ "$#" != 3 ] #Are there less/more than three arguments? 
then
    echo "Error: you provided an incorrect number of arguments." 
    echo "Usage: runmeme.sh directorypath outputname timeinhours"
    exit 1
fi

# Substitute appropriate project name (for Compute Canada) and email address

echo "#!/bin/bash
#PBS -A prj-id-No
#PBS -l walltime=${3}:00:00
#PBS -l nodes=1:ppn=4
#PBS -q xlm2
#PBS -m bea
#PBS -M email@address.com
#PBS -r n
set -eu -o pipefail

">> ${2}


subsetlist=$(ls -v ${1})

mkdir "${1}/output"

# Make sure to substitute appropriate paths

for i in ${subsetlist}
do
    j=$(basename ${i} .fas)
    echo "PATH/TO/meme/bin/meme ${1}/${i} -text -evt 0.05 -dna -mod anr -nmotifs 10 -minw 6 -maxw 10 -maxsites 100 > ${1}/output/${j}.meme" >>${2}
done

qsub ${2}

