#!/bin/bash
set -eu -o pipefail

if [ "$#" != 3 ] #Are there less/more than one arguments? 
then
    echo "Error: you provided an incorrect number of arguments. 
    echo "Usage: make_seederqueue.sh directorypath outputname timeinhours
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

mkdir "${1}/output"

# Make sure to substitute appropriate paths

subsetlist=$(ls -v ${1})
for i in ${subsetlist}
do
    echo "PATH/TO/MEME/meme ${1}/${i} -o ${1}/output/${i} -text -dna -mod anr -nmotifs 10 -minw 6 -maxw 10 -maxsites 100" >>${2}
done

#qsub ${2}

