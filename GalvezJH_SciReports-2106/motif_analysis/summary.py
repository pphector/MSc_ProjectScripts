#!/usr/bin/python
"""
A script that relies on the clustering.py script, but that is specially designed to consolidate
the results of all three motif discovery algorithms. All motifs found by all three algorithms
 will be again clustered and averaged. A report with important information will be written and exported to pdf.  

Requires the following arguments: 
- Location of the directory with all the motif discovery information

Returns:
- A single, consolidated list of motifs
- A .md and .pdf report with a summary of the information found
- A series of .gif images with the weblogos of the clusters found

Dependencies: 
- Requires the clustering.py script to be in the same directory

Author: Hector Galvez
"""

from sys import argv # To be able to parse arguments in the command line
from datetime import date # To be able to write the date in the report
from clustering import clusterinfo,clusteravg,trim # Import clustering functions from the clustering.py script
# Import all relevant TAMO modules
from TAMO import MotifTools 
from TAMO import Clustering
from TAMO.Clustering import MotifCompare
from TAMO.Clustering import Kmedoids

# CLUSTERING
# Define location of all tamo files
listname = str(argv[1].strip().split('/')[-1])
seederloc = argv[1] + '/seeder/' + listname + '_clusters.tamo'
memeloc = argv[1] + '/meme/' + listname + '_clusters.tamo'
weederloc = argv[1] + '/weeder/' + listname + '_clusters.tamo'

#Define output location
tamooutput = argv[1] + '/' + listname + '_allclusters.tamo'

# Define function to open tamo files and return them or an empty list if the tamo file doesn't exist
def opentamo(fileloc):
    '''
    Opens a tamo file with MotifTools.load and returns the list of motifs,
    except when the input file doesn't exist, in which case it returns an empty list. 

    Has 1 argument:
    - fileloc: a string with the location of the file
    '''
    try:
        return MotifTools.load(fileloc)
    except IOError:
        return []

# Import and open all clustered lists
seederlist = opentamo(seederloc)
memelist = opentamo(memeloc)
weederlist = opentamo(weederloc)

# Trim all initial motif lists
# seederlist = trim(seederlist,0.5)
# memelist = trim(memelist,0.5)
# weederlist = trim(weederlist,0.5)

# Create lists of indexes that correspond to each algorithm (for future ID purposes)
seederids = range(len(seederlist))
memeids = range(len(seederlist), len(seederlist)+len(memelist))
weederids = range(len(seederlist) + len(memelist), len(seederlist) + len(memelist) + len(weederlist))

# Create a general list with all the motifs from all algorithms
genlist = []
genlist.extend(seederlist)
genlist.extend(memelist)
genlist.extend(weederlist)

# Perform clustering on the general list of motifs
clusterinf = clusterinfo(genlist)
averages = clusteravg(genlist,clusterinf)

# Trim the final average list
# averages = trim(averages,0.5)
# print clusterinf

# Save new list of cluster averages
MotifTools.save_motifs(averages,tamooutput)

# WEBLOGO IMAGE GENERATION
# Generate giflogos of all average motifs
for index in range(len(averages)):
    cluster = 'Cluster ' + str(index + 1)
    clustergif = argv[1] + '/other/cluster' + str(index + 1)
    averages[index].giflogo(clustergif,title=cluster,scale=2)

# SUMMARY REPORT
# Determine location of the markdown file for the summary report
reportout = open(str(argv[1] + '/final/' + listname + '_cluster_report.md'), 'w')

# Write the header of the report
rundate = date.today()
header = "# Summary report for `" + listname + "`\nThis analysis was run on: " + str(rundate) + \
    '\n\n## Motif clustering and final motifs found\n\n' + \
    '| Motif Cluster | Weblogo | Found by |\n|---------|:--------:|:---------:|'
reportout.write(header)

# Generate table with report for each motif     
for num in range(len(clusterinf[1])):
    clustertitle = 'Motif ' + str(num + 1)
    clusterpng = argv[1] + '/final/cluster' + str(num + 1) + '.png'
    foundin = []
    for item in range(len(clusterinf[1][num])):
        if clusterinf[1][num][item] in seederids and 'Seeder' not in foundin:
            foundin.append('Seeder')
        elif clusterinf[1][num][item] in memeids and 'MEME' not in foundin:
            foundin.append('MEME')
        elif clusterinf[1][num][item] in weederids and 'Weeder' not in foundin:
            foundin.append('Weeder')
        else:
            pass
    report = '\n| **' + clustertitle + '** | ![' + clustertitle + '](' + clusterpng + ') | ' + ' '.join(foundin) + ' |' 
    reportout.write(report)

reportout.close()
