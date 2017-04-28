# Scripts used to Fetch and Generate a "Promoter" Database

## Python script to generate SQLite database 
- genemodel_database.py : python script to generate a small SQLite database containing potato gene names and location of their upstream promoters

## Scripts to parse queries to SQLite database
- genelength.sh : Using output from SQLite database, small script to automatically calculate the length of a list of genes
- getallpromoters.sh : Using outupt from SQLite database, obtain _all_ the promoter sequences (from the *S. tuberosum* genome) from a list of genes
- getpromloc.sh : Using output from SQLite database, obtain _only unique_ promoter sequences (from the *S. tuberosum* genome) form a list of genes

Author: Hector Galvez