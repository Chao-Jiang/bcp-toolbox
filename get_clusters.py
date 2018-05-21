#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 10:07:56 2018

@author: anacoelho
"""
import os
import sys
import numpy as np
from scipy.cluster.hierarchy import fcluster

def get_coords(directory, subject_name, coords_mat, id_roi):
	coords = coords_mat[np.ix_(coords_mat[:,3] == id_roi, np.array([True, True, True, False, False]))]
	return coords

def extract_clusters(linkage_matrix, n, id_roi, roi_name, directory, subject):
    
    # Get clusters from clustering results matrix
    clusters=fcluster(linkage_matrix, n, criterion='maxclust')
    
    # Get coordinates of the roi
    coords_file = os.path.join(directory, subject, 'coords_for_fdt_matrix1')
    coords_mat = np.loadtxt(coords_file)
    coords_roi = get_coords(directory, subject, coords_mat, id_roi)
    
    # Create matrix with coordinates of each voxel and its cluster assignment
    coords_clusters = np.zeros((len(coords_roi),4)) 
    coords_clusters[:,0] = coords_roi[:,0]
    coords_clusters[:,1] = coords_roi[:,1]
    coords_clusters[:,2] = coords_roi[:,2]
    coords_clusters[:,3] = clusters
    
    # Save to separate files
    for i in xrange(1,n+1):
        coords = coords_clusters[np.ix_(coords_clusters[:,3] == i, np.array([True, True, True, False]))]
        output_file = os.path.join(directory, subject,roi_name,'k'+str(n_clusters),'roi'+str(id_roi)+'_cluster'+str(i)+'.txt')
        np.savetxt(output_file, coords, fmt='%d')
        print output_file

#check if we have all arguments
if len(sys.argv) < 5:
    print ('usage: get_clusters <subjects_file> <id_roi> <roi_name> <number_clusters>')
else:

    directory_m1 = '/media/neuroimaging/TOSHIBA/SWBOX_probtrackx/M1/'

    subjects_filepath = str(sys.argv[1])
    with open(subjects_filepath, 'r') as subjects:
        mylist = subjects.read().splitlines()
        for line in mylist:
            # get subject name from file
            subject = line+'_M1'
            print (subject)

            # get id of ROI and file with clustering results
            idroi=int(sys.argv[2])
            roi_name=str(sys.argv[3])
            linkage_mat_name='roi'+str(idroi)+'_results_linkage'
            linkage_mat_filepath = os.path.join(directory_m1, subject, roi_name, linkage_mat_name)
            linkage_mat = np.loadtxt(linkage_mat_filepath)
            
            # get clusters and save to files
	    n_clusters=int(sys.argv[4])
            extract_clusters(linkage_mat, n_clusters, idroi, roi_name, directory_m1, subject)
	    
