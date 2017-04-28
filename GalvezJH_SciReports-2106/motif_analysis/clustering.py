#!/usr/bin/python 
"""
A series of functions that can be useful for clustering motifs using the kmedoids implementation from TAMO.

Dependencies: 
- The following modules from the TAMO suite: 
    - MotifTools
    - Clustering
    - Clustering.MotifCompare
    - Clustering.Kmedoids

Author: Hector Galvez
"""

# Import all relevant TAMO modules
from TAMO import MotifTools
from TAMO import Clustering
from TAMO.Clustering import MotifCompare
from TAMO.Clustering import Kmedoids

def clusterinfo(motiflist):
    """
    Performs the Best Kmedoids implementation from the TAMO.Clustering module on a list of motif
    and returns a new list of motifs that are the cluster averages of the clusters found. 

    Has 1 argument: 
    - motiflist: a *list* of motifs that will be clustered

    Returns:
    - clusteraverage: a *new* list with only the averages of every cluster found
    """
    # Calculate the distance matrix of the motifs in the initial file
    motifDmat = Clustering.MotifCompare.computeDmat(motiflist)  
    # Set a variable for the max number of clusters (kmax), which will be the total number of sig motifs
    initk = len(motiflist)
    # Parameters are taken from the documentation examples set by the original code
    bestKmedoids = Clustering.Kmedoids.bestKMedoids_cluster(motifDmat, 
        kmax=initk, num_cycles=10, max_kMedoids_iterations=1000, min_dist=0.1499999999,
        seeds=None, verbose=0, print_fnctn=None, data=None) 
    return bestKmedoids

def clusteravg(motiflist,kmedoids):
    '''
    A function that returns the cluster averages from a list of motifs and its bestKmedoids
    
    Has 2 arguments:
    - initlist: a list of motifs that will be used to compute the averages
    - kmedoids: a variable holding the results of a bestKmedoids run

    Returns:
    - clusteraverage: a new list with the *trimmed* averages of every cluster 
                    or the medoid of a cluster whose trimmed average is too small
    '''
    # Create output list variable 
    clusteraverage = []
    # Create averages of the motifs found in each cluster
    for indices in kmedoids[1]:
        # Create a list with all the motifs in a cluster
        cluster = []
        #print 'This is cluster ' + str(indices + 1) + ':'
        for index in kmedoids[1][indices]:
            cluster.append(motiflist[index])
        
        average = Clustering.MotifCompare.averagemotifs(cluster,VERBOSE=0)
        trimmedaverage = average.trimmed(thresh=0.5)
        
        # If the trimmed average is too small (i.e. has less than 5 bp)
        # it will be ignored. 
        if len(trimmedaverage) >= 5:
            clusteraverage.append(trimmedaverage)
        else:
            medoid = motiflist[kmedoids[0][indices]]
            clusteraverage.append(medoid)
    return clusteraverage

def trim(motiflist,threshold):
    '''
    A function that receives a list of TAMO motifs and returns the same list with motifs that
    have trimmed edges that contain low information content. 

    Has 2 arguments: 
    - motiflist: the list of motifs that will be trimmed
    - threshold: (float) the minimun threshold in bits that will be allowed in the motif

    Returns:
    - The same list of motifs, only they will have their edges trimmed
    '''
    # Verify threshold is float
    try:
        threshold = float(threshold)
    except ValueError:
        print 'Problem with threshold!'
        return None
    # Cycle trough each element of the initial list
    for num in range(len(motiflist)):
        # Make sure that trimming doesn't result in a motif that is shorter than 5bp
        if len(motiflist[num].trimmed(thresh=threshold)) <= 5:
            toosmall.append(num)
        else:
            motiflist[num] = motiflist[num].trimmed(thresh=threshold)
    return motiflist
