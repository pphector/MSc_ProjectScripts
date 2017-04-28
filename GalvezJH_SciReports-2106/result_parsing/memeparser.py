#!/usr/bin/python
"""
MEME parser using TAMO tools to create objects with all the significant motifs in a meme result file.
Requires TAMO to be installed to work. 

Has 2 arguments:
- Path to subset result directory without trailing '/' (str)
- Significance (float)

Returns:
- A Tamo file with the saved significant motifs

Dependencies:
- The file Stuberosum.py in the same directory with the variable 'bkgrddict'

Author: Yevgen Zolotarov
Updates: Hector Galvez
"""

from sys import argv # To be able to parse arguments in the command line
import glob # To access the contents of a directory
from Bio import motifs  # BioPython 1.61+ is required
from TAMO import MotifTools # TAMO is required
from Stuberosum import bkgrddict # To avoid inputing the background, it is imported

#Define gene list name for further use in output files
genelist = argv[1].split('/')[-2]

#Output variable
sigmotifs = []

#Declare variables for easy parsing
lines = '-' * 80
stars = '*' * 80
matrixtitle = 'position-specific probability' # Defined as a variable so it can be changed
nucleotides = ['A','C','G','T']

# CONSUMER FUNCTIONS
# Define consumer function to output motifs in TAMO format
def tamoinput(mememat,filename):
    '''
    A small function to turn a list parsed from the memefile into a 
    TAMO compatible list of dictionaries for its input.
    *Only works for position-specific matrices*

    Has two arguments: 
    - The string of the position-specific probability matrix in the meme file
    - The name of the file where the matrix is coming from
    Returns:
    - A list with the first element containing the file where the motif was found
    '''
    output = [str(filename)]
    for item in mememat.strip().split('\n')[1:]:
        row = {}
        values = item.strip().split()
        for num in range(len(values)):
            row[nucleotides[num]] = float(values[num])
        output.append(row)
    return output

def significance(mememat,signif):
    '''
    A small function to determine if the motif is acutally significant based on a user provided 
    significance threshold.

    Has two arguments: 
    - The string of the matrix in the meme file
    - The user-provided float to determine significance
    Returns:
    - True of false, depending on wether or not it is significant
    '''
    # Make sure signiticance is a float
    signif = float(signif)
    # Parse the string to obtain a float equal to the evalue
    evalue = float(mememat.strip().split('\n')[0].split('=')[-1].strip())
    # If the evalue is lower than the significance threshold return True, else return False
    if evalue <= signif:
        return True
    else:
        return False

# SCANNER FUNCTION
# Parse each file in the directory with all the subset results
for subset in glob.glob(str(argv[1]) + '/*meme'):
    subsetfile = open(subset, 'r')
    
    #Only meme files with motifs that passed the meme stringency value have "lines", 
    #so by separating using lines we can know if there are potential motifs to parse
    subsetdata = subsetfile.read().split(lines) 

    #If there are potential motifs in the file, proceed to parse the probability matrix 
    if len(subsetdata) > 1:
        for num in range(len(subsetdata)):
            # Find the portion of the file with the appropriate matrix to parse (defined by matrixtitle)
            if subsetdata[num].find(matrixtitle) != -1:
                # Determine if the motif is *actually* significant
                if significance(subsetdata[num+1],argv[2]):
                    # Add the TAMO formated dictionary into the sigmotifs list variable
                    sigmotifs.append(tamoinput(subsetdata[num+1],subset))
                else:
                    pass
            else:
                pass
    else:
        pass

if len(sigmotifs) > 0:
    #Define output files
    #First output is a text file for STAMP
    #output1 = open(argv[2] + "/" + genelist + ".stamp",'w')
    #Second format is a tamo file with the motifs contained
    output2 = argv[1] + "/" + genelist + ".tamo"

    # TAMO CONVERSION
    # TAMO formated list of files
    tamomotifs = []

    # Convert dictionaries found in sigmotifs and store them as TAMO motifs 
    for motif in sigmotifs:
        tamomotif = MotifTools.Motif_from_counts(motif[1:],beta=0.01,bg=bkgrddict)
        tamomotifs.append(tamomotif)

    MotifTools.save_motifs(tamomotifs,output2)
    # output1.close()
else:
    print "MEME didn't find any significant motifs for this list: %s" % genelist