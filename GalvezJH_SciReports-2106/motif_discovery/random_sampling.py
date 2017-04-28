#!/usr/bin/python

'''
#Random Subsets Tool
Tool for generating random subsets of a file with a list of sequences (promoters). 
Requires three arguments:
1. The initial input file. 
2. The number of subgroups required. 
3. The filename of the subgroups. 

*Developed by P. Munasamy with contributions from  H. Galvez.*
'''
from sys import argv
import random

#Use argv library to open the first argument as the file
with open(argv[1]) as f:
    file = f.read()

#Create an list of sequences by splitting the initial file using the '>' as delimiters
seq_ind = file.split(">")
#Remove the '>' character from the split elements 
seq_ind.pop(0)

#Create a list of numbers, each representing a seq from the split file
number_of_sequences = [i for i in range(len(seq_ind))]

subset_total = int(argv[2]) # number of subset files to create

#Loop through through the list of the total files that are to be created 
for i in range(subset_total):
#Create a name for the file where the sub-list will be saved using the third argument
    filename = str(argv[3]) + "_subset_%s.fas" % i
#Create a list of random numbers from the number_of_sequences variable
    rand_sample = random.sample(number_of_sequences, 10) # take 10 random numbers without replacement
#Now actually create the output file
    output = open(filename, "w")
#For every number in the random number list
    for j in rand_sample:
#Add the '>' character (which was removed) and the rest of the seq that correspond to number j
        seq = ">" + seq_ind[j]
#Write the seq to the output
        output.write(seq)
#When finished, close the file
    output.close()
