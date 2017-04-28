#!/usr/bin/python
'''
Weeder parser using TAMO to create objects with all the motifs in a Weeder result file.

Has 1 argument: 
- Path to weeder result directory without trailing '/' (str)

Returns 1 files:
- A TAMO file with the significant motifs as TAMO motif objects

Dependencies:
- The file Stuberosum.py in the same directory with the variable 'bkgrddict'

Author: Hector Galvez
'''

from sys import argv # To be able to parse arguments in the command line
import glob # To access the list of files in a directory
from TAMO import MotifTools # To make use of TAMO tools for clustering and more
from Stuberosum import bkgrddict # To avoid inputing the background, it is imported

# Define gene list name for further use in oputut files
genelist = argv[1].split('/')[-2]

# Define output file
output = argv[1] + '/' + genelist + '.tamo'

# SCANNER FUNCTION
# Define intermediate variables
blankindex = None

# Start parsing file, separate each motif into different list element
inputfile = glob.glob(str(argv[1]) + '/*matrix.w2')[0]
motiflist = open(str(inputfile), 'r').read().split('>')

# Separate each motif into lists of one line each
for num in range(len(motiflist)):
    if motiflist[num] != '':
        motiflist[num] = motiflist[num].strip().split('\n')
    elif motiflist[num] == '':
        blankindex = num

# Remove any blank items from the list 
motiflist.pop(blankindex)

# Build matrix dictionaries and substitute the strings for the dictionaries
for num in range(len(motiflist)):
    # Prepare emtpy list of dictionaries of the length of the motif
    tempmotif = []
    motiflength = len(motiflist[num][1].strip().split('\t')) - 1
    for item in range(motiflength):
        tempmotif.append({})
    # Start filling in the dictionaries with the information in the matrix
    for line in range(1,5):
        nucleotide = motiflist[num][line].strip().split('\t')[0]
        problist = motiflist[num][line].strip().split('\t')[1:]
        for position in range(motiflength):
            tempmotif[position][nucleotide] = float(problist[position])
    # Save the list of dictionaries in the general variable
    motiflist[num] = tempmotif
 
#print motiflist

# TAMO CONVERSION
# TAMO formated list of files
tamomotifs = []

# Convert dictionaries found in sigmotifs and store them as TAMO motifs 
for motif in motiflist:
    tamomotif = MotifTools.Motif_from_counts(motif[:],beta=0.01,bg=bkgrddict)
    tamomotifs.append(tamomotif)

MotifTools.save_motifs(tamomotifs,output)
