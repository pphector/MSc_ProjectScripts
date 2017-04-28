# Scripts used to Prepare and Run Motif Discovery Software

- accesssion_lists.sh : script to automatically generate a list with only names of gene IDs to be analyzed for motif discovery
- create_finder.sh : scritp to automate finder files (required for Seeder) for many lists of genes
- create_stndln_finder.sh : script to generate a finder file (required for Seeder) for a single list of gene
- make_memequeue.sh : script to automate appropriately formatted bash scripts for to run MEME using Torque on Compute Canada server
- make_seederqueue.sh : script to automate appropriately formatted bash scripts for to run Seeder using Torque on Compute Canada server
- make_subsets.sh : script to perform random sampling of large lists of genes to increase probability of finding motifs
- runmeme.sh : script to automate generation of a single bash script to run MEME using Torque on Compute Canada server
- runseeder.sh : script to automate generation of a single bash script to run Seeder using Torque on Compute Canada server
- random_sampling.py : python script required to automate random sampling of a list of genes

Author: Hector Galvez