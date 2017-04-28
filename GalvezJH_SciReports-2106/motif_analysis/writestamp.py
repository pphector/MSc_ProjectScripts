#!/usr/bin/python
'''
This opens a general TAMO cluster list and outputs **TO STANDARD OUT** the probability matrices of all
items there. Separated by a line with the name of each cluster. *It is recommended to be used in a
bash pipeline where the standard out can be written into a file.*  

Has 1 argument: 
- motiflist: a TAMO motif list that will be outputed 

Returns: 
- A series of strings that represet the probability matrices of all motifs in the input list

Author: Hector Galvez
'''

from sys import argv
from TAMO import MotifTools

# Open list
motiflist = MotifTools.load(argv[1])

# Start printing information for each motif
for num in range(len(motiflist)):
    print '>Cluster_' + str(num + 1)
    motiflist[num]._print_p()

