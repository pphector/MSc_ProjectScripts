#!/usr/bin/python

"""
Database creation for unified motif and promoter storage. 
Has 2 arguments: 
- Name and address of output database
- Input data in a space delimited format
"""
import sys
import sqlite3
from collections import OrderedDict

#Filename of SQLite Database based on first argument 
db_name= sys.argv[1]

#Initialize database connection
conn= sqlite3.connect(db_name)
c= conn.cursor()

#CREATE GENE-MODELS TABLE
#Write schema commands
genetable_def= '''\
CREATE TABLE genemodels(
    id integer primary key,
    geneid text,
    chrom text,
    start integer,
    end integer,
    strand text,
    promoter text);
'''

#Execute the create table command
c.execute(genetable_def)

#LOAD DATA INTO TABLE
#Table columns with data type (id not included, automatic)
tbl_cols= OrderedDict([("geneid",str),("chrom",str),
    ("start",int),("end",int),("strand",str),("promoter",str)])

with open(sys.argv[2]) as input_file:
    for line in input_file:
        #Split tab delimited line
        values = line.strip().split()

        #Calculate promoter location
        if values[4]=='+':
            prom_start = int(values[2])-1000
            promloc = str(values[1]) + ":" + str(prom_start) + "-" + str(values[2])
            values.append(promloc)
        elif values[4]=='-':
            prom_end = int(values[3])+1000
            promloc = str(values[1]) + ":" + str(values[3]) +  "-" + str(prom_end)
            values.append(promloc)    
        else:
            raise ValueError("Strand information incorrect")
            
        #Pair each value with column name
        cols_values = zip(tbl_cols.keys(), values)

        #Use column name to look up appropriate function to coerce 
        #values to appropriate type
        coerced_values= [tbl_cols[col](value) for col, value in cols_values]

        #Create empty list of placeholders
        placeholders = ["?"] * len(tbl_cols)

        #Create query by joining column names and placeholders quotation
        #marks into comma-separated strings
        colnames = ", ".join(tbl_cols.keys())
        placeholders = ", ".join(placeholders)
        query = "INSERT INTO genemodels(%s) VALUES (%s);" % (colnames, placeholders)

        #Execute query
        c.execute(query,coerced_values)

#Commit changes and close database
conn.commit()
conn.close()