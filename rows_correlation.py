#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 11:29:27 2018

@author: anacoelho
"""
import sys
import os
import time
import numpy as np
import subprocess

def file_len(fname):
    p = subprocess.Popen(['wc', '-l', fname], stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE)
    result, err = p.communicate()
    if p.returncode != 0:
        raise IOError(err)
    return int(result.strip().split()[0])

def compute_cc_mat(ids_roi, sparse_mat, length, output_mat):
    i,j,value = np.loadtxt(sparse_mat).T
    
    # create dictionary to store connectivity pattern of each voxel
    arrays={}
    nr_voxels=len(ids_roi)
    #print (nr_voxels)
    for id in range(len(ids_roi)):
        arrays[id] = np.zeros((1,length))
    # get connectivity pattern of each voxel from sparse matrix and save to dictionary
        for x in range(len(i)):
            if (i[x]==ids_roi[id]):
		#print (id)
                col=int(j[x]-1)
                row=arrays.get(id)
                row[0][col]=value[x]
                arrays.update({id:row})
    print ('Dictionary created!')

    print(len(arrays.keys()))
    # compute correlation between each pair of voxels
    correlation_mat = np.zeros((nr_voxels,nr_voxels))
    for key in arrays:
        v1 = arrays.get(key)
	#print(len(v1[0]))
        for key2 in arrays:
            v2 = arrays.get(key2)
	    #print(len(v2[0]))
            correlation_mat[key][key2]=1 - np.corrcoef(v1[0],v2[0])[0][1]
 	    #print(np.corrcoef(v1[0],v2[0])[0][1])
        #print np.corrcoef(v1[0],v2[0])[0][1], key, key2.
    print ('Correlation matrix created!')
    np.savetxt(output_mat, correlation_mat)
  
#check if we have all arguments
if len(sys.argv) < 3:
    print ('usage: rows_correlation <subjects_file> <id_roi>')
else:

    directory_m1 = '/media/neuroimaging/TOSHIBA/SWBOX_probtrackx/M1/'
    
    subjects_filepath = str(sys.argv[1])
    with open(subjects_filepath, 'r') as subjects:
        mylist = subjects.read().splitlines()
        for line in mylist:
            # get subject name from file
            subject = line+'_M1' 
            print (subject)
            
            # get id of ROI and file with voxel ids 
            idroi=str(sys.argv[2])
            id_roi_name='ids_roi'+idroi+'.txt'
            ids_roi_filepath = os.path.join(directory_m1, subject,id_roi_name)
            ids_roi = np.loadtxt(ids_roi_filepath)
            
            # get sparse mat file
            sparse_mat_name='roi'+idroi+'_sparse_mat'
            sparse_mat_file = os.path.join(directory_m1, subject,sparse_mat_name)
            
	    # get id of last voxel of fdt_matrix1.dot (it will be the length of each voxel vector of connectivity)
	    fdt_mat_filepath = os.path.join(directory_m1, subject,'fdt_matrix1.dot')
            line1 = subprocess.check_output(['tail','-1',fdt_mat_filepath])
	    l = line1.split()
	    length = int(l[0]) 
	    print (length)

            # get output file name
            output_name='roi'+idroi+'_cc_mat'
            output_mat_file = os.path.join(directory_m1, subject,output_name)
            
            # compute correlation matrix
            compute_cc_mat(ids_roi, sparse_mat_file, length, output_mat_file) 
        
