#!/usr/bin/python
"""
A script for reducing the redundancy of a series of motifs, using the kmedoids implementation from TAMO.

Requires the following number of arguments:
- The location of the *single* TAMO motif file that was created after parsing motifs. 

Returns: 
- A new TAMO motif file containing only the cluster averages

Dependencies:
- Requires the clustering.py script to be in the same directory

Author: Hector Galvez
"""

from sys import argv,exit # To be able to parse arguments in the command line
from clustering import clusterinfo,clusteravg # Import clustering functions from clustering.py script
# Import all relevant TAMO modules
from TAMO import MotifTools
from TAMO import Clustering
from TAMO.Clustering import MotifCompare
from TAMO.Clustering import Kmedoids

try:
    # Import the motif lists from the tamo file provided as the first argument
    inputlist = MotifTools.load(argv[1])
except IOError:
    print "Couldn't find %s, moving on..." % str(argv[1].split('/')[-2] + '/' + argv[1].split('/')[-1])   
    exit() 

# Create the name of a new TAMO file for clustered motifs
genelist = str(argv[1].split('/')[-3])
output = argv[1].rstrip(genelist + '.tamo') + genelist + '_clusters.tamo'

# Create output information
clusterinf = clusterinfo(inputlist)
averages = clusteravg(inputlist,clusterinf)

# Save new list of cluster averages
MotifTools.save_motifs(averages,output)

