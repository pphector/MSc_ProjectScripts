#!/usr/bin/python

'''
A scritp to rapidly create a list of gene locations for easy query with faidx
Has 2 arguments: 
- Location of genemodels database
- Input list of gene accession id's 

**Important**
The input list is expected to have a header, so the first row will be elimianted. If this is not the case, please add a blank first row to your list of gene accession ids
'''

import sys 
import sqlite3

#Filename of SQLite Database based on the first argument
db_name = sys.argv[1]

#Define output filename 
output = open(str(sys.argv[2].split('/')[-1].strip('.txt')) + '.tbl','w')
output.write("GeneID\tChromosome\tStrand\tStart\tEnd\tDescription\n")

#Initialize database connection
conn = sqlite3.connect(db_name)
c = conn.cursor()

#Read list of genes
genes = open(str(sys.argv[2]),'r').read()
genelist = []
genelist = genes.strip().split('\n')[1:] # !!REMOVE GENELIST HEADER!!

#Query the database one gene accession id at a time
for gene in genelist:  
#Query statement
    statement = 'SELECT geneid, chrom, strand, start, end FROM genemodels WHERE geneid == "%s";'%(gene)
#Execute the query statement
    c.execute(statement)
#Save query result into an easy to manipulate list
    result = []
    rawresult = c.fetchone()
    for num in range(len(rawresult)):
        result.append(str(rawresult[num]))
#Use list to write output in a file in the correct format for faidx
    output.write("\t".join(result) + "\n")

#Close open files
output.close()
conn.close()

