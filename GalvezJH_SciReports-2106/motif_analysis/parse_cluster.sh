#!/bin/bash
set -eu -o pipefail 
# Script integrating all parse methods into a single pipeline. 
# Generates a tamo file for each motif discovery algorithm.
# Consolidates all motifs from each method into clusters.
# Clusters all motifs from all methods. 
# Generates a report of the clustered motifs. 
# Dependencies include ipython for the drawing phase. 

# INPUT
# Check input
if [ "$#" != 3 ] # Are there less/more than three arguments? 
then
    echo "Error: you provided an incorrect number of arguments"
    echo "Usage: parse_cluster.sh directorypath seedersignificance memesignificance"
    exit 1
fi

# Define input variables
genelist=$(basename ${1})
seederloc=${1}/seeder
memeloc=${1}/meme
weederloc=${1}/weeder
seedersig=${2}
memesig=${3}
promlistloc=${1}/${genelist}.rvcomp.prom.fasta

# Start message
echo "Starting pipeline for ${genelist}"

# PARSING
echo "Parsing..."
#   Seeder 
python seederparser.py ${seederloc} ${seedersig}
#   Meme
python memeparser.py ${memeloc} ${memesig}
#   Weeder
python weederparser.py ${weederloc}

# CLUSTERING
echo "Clustering results of each algorithm..."
#   Seeder
python clusterone.py ${seederloc}/${genelist}.tamo
#   Meme
python clusterone.py ${memeloc}/${genelist}.tamo
#   Weeder
python clusterone.py ${weederloc}/${genelist}.tamo

# REPORT
echo "Clustering all results..."
#   Compute overall motifs and begin writing report
python summary.py ${1}

#   Convert weblogos into pngs for use in pdf
for item in $(ls -v ${1}/other)
do
    clustername=$(basename ${item} .gif)
    convert ${1}/other/${item} -resize 200x60 ${1}/final/${clustername}.png 
done

#   Generate the text file for input in STAMP
echo "Creating stamp file..."
python writestamp.py ${1}/${genelist}_allclusters.tamo > ${1}/annot/${genelist}_stamp.tmp
python formatstamp.py ${1}/annot/${genelist}_stamp.tmp

#   Location in promoters
echo "Mapping the motifs in the promoters..."
python prepsitemap.py ${1}
oneletters=$(cat ${1}/other/${genelist}_oneletter.tmp)
symbols=$(cat ${1}/other/${genelist}_symbols.tmp)

# Try to see if it is possible to use the tamo motif file directly instead of oneletters
python $TAMO/Sitemap.py -f ${promlistloc} -t 0.8 -L ${symbols} -m ${1}/${genelist}_allclusters.tamo >> ${1}/annot/${genelist}_sitemap.txt

ipython drawmotifmaps.py ${promlistloc} ${1}/annot/${genelist}_sitemap.txt >> ${1}/final/${genelist}_cluster_report.md

#   Compile markdown summary into pdf and html
echo "Finishing reports..."
pandoc -o ${1}/final/${genelist}_report.pdf ${1}/final/${genelist}_cluster_report.md
pandoc -o ${1}/final/${genelist}_report.html ${1}/final/${genelist}_cluster_report.md

# End message
echo "Successfully finished running pipeline for ${genelist}"
