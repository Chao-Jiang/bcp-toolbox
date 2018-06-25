#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 10:07:56 2018

@author: anacoelho
"""
import os
import sys
import numpy as np
import scipy.io as sio
from scipy.cluster.hierarchy import fcluster

def get_coords(directory, subject_name, coords_mat, ids_mat, id_roi):
	coords = coords_mat[np.ix_(coords_mat[:,3] == id_roi-1 , np.array([True, True, True, False, True]))]
	
	#print(len(coords))
	bad_ids=[]
	for i in xrange(len(coords)):
		if coords[i,3] not in ids_mat:
			bad_ids.append(i)
			#print(coords[i,:])

	coords = np.delete(coords, bad_ids, axis=0)
	#print(len(coords))
	return coords

def extract_clusters(linkage_matrix, n, id_roi, data_directory, working_directory, subject, roi_name):
	
	# Get clusters from clustering results matrix
	clusters=fcluster(linkage_matrix, n, criterion='maxclust')
	
	# Get coordinates of the roi
	coords_file = os.path.join(data_directory, subject, 'coords_for_fdt_matrix1')
	coords_mat = np.loadtxt(coords_file)
	ids_file = os.path.join(working_directory, subject, 'roi'+str(id_roi)+'_ids.mat')
	mat_contents = sio.loadmat(ids_file)
	mat = mat_contents['ids']
	ids_mat = np.array(mat)

	coords_roi = get_coords(working_directory, subject, coords_mat, ids_mat, id_roi)
	# Create matrix with coordinates of each voxel and its cluster assignment
	coords_clusters = np.zeros((len(coords_roi),4)) 
	coords_clusters[:,0] = coords_roi[:,0]
	coords_clusters[:,1] = coords_roi[:,1]
	coords_clusters[:,2] = coords_roi[:,2]
	coords_clusters[:,3] = clusters
	
	# Save file with coordinates and cluster number
	output_file = os.path.join(working_directory, subject,roi_name,'k'+str(n)+'_roi'+str(id_roi)+'_clusters.txt')
	np.savetxt(output_file,coords_clusters, fmt='%d')
	
	# Save to separate files
	#for i in xrange(1,n+1):
	#    coords = coords_clusters[np.ix_(coords_clusters[:,3] == i, np.array([True, True, True, False]))]
	#    output_file = os.path.join(working_directory, subject,'k'+str(n)+'_roi'+str(id_roi)+'_cluster'+str(i)+'.txt')
	#    np.savetxt(output_file, coords, fmt='%d')
		#print output_file

#check if we have all arguments
if len(sys.argv) < 7:
	print ('usage: get_clusters <working_dir> <data_dir> <subjects_file> <roi_name> <id_roi_l> <id_roi_r> <max_nr_clusters')
else:
	# get directories
	working_dir = str(sys.argv[1])
	data_dir = str(sys.argv[2])

	subjects_filepath = str(sys.argv[3])
	with open(subjects_filepath, 'r') as subjects:
		mylist = subjects.read().splitlines()
		for line in mylist:
			# get subject name from file
			subject = line
			print (subject)

			# get id of ROI and file with clustering results
			# left
			idroi_l=int(sys.argv[5])
			linkage_mat_l_name='roi'+str(idroi_l)+'_results_linkage'
			linkage_mat_l_filepath = os.path.join(working_dir, subject, linkage_mat_l_name)
			linkage_mat_l = np.loadtxt(linkage_mat_l_filepath)

			# right
			idroi_r=int(sys.argv[6])
			linkage_mat_r_name='roi'+str(idroi_r)+'_results_linkage'
			linkage_mat_r_filepath = os.path.join(working_dir, subject, linkage_mat_r_name)
			linkage_mat_r = np.loadtxt(linkage_mat_r_filepath)
			
			roi_name = str(sys.argv[4])
			# get clusters and save to files
			max_n_clusters=int(sys.argv[7])
			for i in xrange(2,max_n_clusters+1):
				# left
				extract_clusters(linkage_mat_l, i, idroi_l, data_dir, working_dir, subject, roi_name)
				# right
				extract_clusters(linkage_mat_r, i, idroi_r, data_dir, working_dir, subject, roi_name)

			
		
