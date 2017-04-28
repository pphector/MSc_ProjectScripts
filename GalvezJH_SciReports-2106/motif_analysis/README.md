# Scritps use to Analyze and Draw Figures for Motif Discovery

- clustering.py : series of functions that can be useful for clustering motifs using the kmedoids implementation from TAMO
- clusterone.py : script for reducing the redundancy of a series of motifs, using the kmedoids implementation from TAMO
- draw_weblogos.py : script that only draws high quality motif weblogos and saves them as a .gif file
- drawmotifmaps.py : script that takes the information generated by the sitemap.py script and generates a diagram
with the location of the motifs found signalled in a more understandable way
- formatstamp.py : script to format the output of a writestamp.py script into a format that will be appropriate for STAMP analysis
- parse_cluster.sh : script integrating all parse methods into a single pipeline. 
- prepsitemap.py : simple script to prepare two files for their use in the sitemap.py command
- summary.py : A script that relies on the clustering.py script, but that is specially designed to consolidate
the results of all three motif discovery algorithms
- writestamp.py : This opens a general TAMO cluster list and outputs **TO STANDARD OUT** the probability matrices of all items there

Author: Hector Galvez