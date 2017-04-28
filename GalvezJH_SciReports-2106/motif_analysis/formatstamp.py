#!/usr/bin/python
'''
A script to format the output of a writestamp.py script into a format that will be appropriate for STAMP analysis.

Has 1 argument: 
- filein: Location to a .tmp file with the probability matrices separated by lines that start with '>'

Returns:
- A new text file that has the appropriate format for STAMP analysis 
'''

from sys import argv

# Define output name
outname = argv[1].split('.')[-2] + '.txt'

# Open input file for reading 
infile = open(argv[1],'r')

# Open output file for writing
outfile = open(outname,'w')

# Start parsing and writing the output file 
for line in infile:
    linein = str(line)
    if linein[0] == '>':
        outfile.write(linein)
    elif linein[1] == 'A' or linein[1] == 'C' or linein[1] == 'T' or linein[1] == 'G':
        outfile.write(linein[1:])
    else:
        pass

# Close all files
outfile.close()
infile.close()
