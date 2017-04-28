#!/usr/bin/python
"""
A script that only draws high quality motif weblogos and saves them as a .gif file. 

Requires the following arguments: 
- The location of a tamo motif file which contains the motifs to be drawn

Returns:
- A series of .gif images with the weblogos of the motifs in the input

Author: Hector Galvez
"""

from sys import argv # To be able to parse arguments in the command line
# Import all relevant TAMO modules
from TAMO import MotifTools 
from TAMO import Clustering
from TAMO.Clustering import MotifCompare
from TAMO.Clustering import Kmedoids

# CLUSTERING
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

# Create a general list with all the motifs 
inputloc = argv[1]
inputlist = opentamo(inputloc)

# WEBLOGO IMAGE GENERATION
# Generate giflogos of all average motifs
for index in range(len(inputlist)):
    cluster = 'Motif ' + str(index + 1)
    clustergif = './motifs/motif' + str(index + 1)
    inputlist[index].giflogo(clustergif,title=cluster,scale=3)

