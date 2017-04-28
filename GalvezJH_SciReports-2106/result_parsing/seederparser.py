#!/usr/bin/python
'''
Seeder parser using seedertools to create objects with all the significant motifs in a seeder result file.
Requires the seedertools.py file to be in the same directory.

Has 2 arguments: 
- Path to seeder motif directory without final '/' (str)
- Significance (float)

Returns two files:
- A list of significant seeder motif objects formatted for search with STAMP
- A TAMO file with the significant motifs as TAMO motif objects

Dependencies:
- The file Stuberosum.py in the same directory with the variable 'bkgrddict'

Author: Hector Galvez
'''

from sys import argv # To be able to parse arguments in the command line
import seedertools # To properly parse seeder files
import glob # To access the list of files in a directory
from TAMO import MotifTools # To make use of TAMO tools for clustering and more
from Stuberosum import bkgrddict # To avoid inputing the background, it is imported

#Define gene list name for further use in output files
genelist = argv[1].split('/')[-2]



#Parse significant motifs from all subsets results in seedertools
sigmotifs = []

for subset in glob.glob(str(argv[1]) + '/*finder'):
    sigmotif = seedertools.seeder_parser(open(subset,'r'), float(argv[2]))
    if sigmotif != []:
        sigmotifs += sigmotif
    else: 
        pass

# If there were any significant motifs, save them as a tamo and stamp file
if len(sigmotifs) > 0:
    #Define output files
    #First output is a text file for STAMP
    output1 = open(argv[1] + "/" + genelist + ".stamp",'w')
    #Second format is a tamo file with the motifs contained
    output2 = argv[1] + "/" + genelist + ".tamo"

    #Prepare a file for input in STAMP
    for motif in sigmotifs:
        output1.write(motif.stampmatrix('NFM') + "\n")


    #Turn seeder motifs into tamo format for further functionality
    tamomotifs = []

    for motif in sigmotifs:
        #print motif.stdmatrix('NFM')
        tamomotif = MotifTools.Motif_from_counts(motif.nfm,beta=0.01,bg=bkgrddict)
        tamomotifs.append(tamomotif)

    MotifTools.save_motifs(tamomotifs,output2)

    output1.close()
else:
    print "Seeder found no significant motifs for this list: %s" % genelist