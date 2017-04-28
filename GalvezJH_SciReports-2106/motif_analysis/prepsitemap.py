#!/usr/bin/python
'''
Simple script to prepare two files for their use in the sitemap.py command. 

Has 1 argument:
- motiflist: a tamo list of the clusters that will be mapped (allclusters) 

Returns: 
- One file with a long string of one letter summaries of each cluster average
- One file with the characters that will be used to represent all cluster averages

Author: Hector Galvez
'''

from sys import argv
from TAMO import MotifTools

# Prepare output names
genelist = argv[1].split('/')[-1]
allclusters = argv[1] + '/' + genelist + '_allclusters.tamo'
#print genelist
oneletters = argv[1] + '/other/' + genelist + '_oneletter.tmp'
symbols =  argv[1] + '/other/' + genelist + '_symbols.tmp'

# Open output files for writing
oneletters = open(oneletters,'w')
symbols = open(symbols,'w')

# Define output variables
oneletterlist = []
symbolstring = '1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ*+.,:;!'

# Open list
motiflist = MotifTools.load(allclusters)

# Try to verify the initial list is not too long
if len(motiflist) > len(symbolstring):
    # If the list is too long, raise an exception so that the program quits
    raise ValueError("The cluster list is too long for sitemap.py")
# If the list is not too long, adjust the symbols string to the appropriate length
else:
    symbolstring = symbolstring[:len(motiflist)]

# Save symbol string in the symbols file and close that file
symbols.write(symbolstring)
symbols.close()

# Add oneletter summaries to the list
for num in range(len(motiflist)):
    oneletterlist.append(motiflist[num].oneletter)

# Write the list (separated by commas) of one letter summaries into the output file and close
oneletters.write(','.join(oneletterlist))
oneletters.close()
