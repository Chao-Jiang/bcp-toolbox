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
    for id in range(len(ids_roi)):
        arrays[id] = np.zeros((1,length))
    # get connectivity pattern of each voxel from sparse matrix and save to dictionary
        for x in range(len(i)):
            if (i[x]==ids_roi[id]):
                col=int(j[x]-1)
                row=arrays.get(id)
                row[0][col]=value[x]
                arrays.update({id:row})
    print ('Dictionary created!')

    #print(len(arrays.keys()))

    # compute correlation between each pair of voxels
    correlation_mat = np.zeros((nr_voxels,nr_voxels))
    for key in arrays:
        v1 = arrays.get(key)
        for key2 in arrays:
            v2 = arrays.get(key2)
            #correlation_mat[key][key2]=1 - abs(np.corrcoef(v1[0],v2[0])[0][1])
            correlation_mat[key][key2] = np.corrcoef(v1[0],v2[0])[0][1]
    print ('Correlation matrix created!')
    np.savetxt(output_mat, correlation_mat)
  
#check if we have all arguments
if len(sys.argv) < 6:
    print ('usage: rows_correlation <working_dir> <data_dir> <subjects_file> <id_roi_l> <id_roi_r>')
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
            
            # get id of ROIs and files with voxel ids 
            # left
            idroi_l=str(sys.argv[4])
            id_roi_l_name='ids_roi'+idroi_l+'.txt'
            ids_roi_l_filepath = os.path.join(working_dir, subject,id_roi_l_name)
            ids_roi_l = np.loadtxt(ids_roi_l_filepath)
            
            # right
            idroi_r=str(sys.argv[5])
            id_roi_r_name='ids_roi'+idroi_r+'.txt'
            ids_roi_r_filepath = os.path.join(working_dir, subject,id_roi_r_name)
            ids_roi_r = np.loadtxt(ids_roi_r_filepath)

            # get sparse mat file
            # left
            sparse_mat_l_name='roi'+idroi_l+'_sparse_mat'
            sparse_mat_l = os.path.join(working_dir, subject,sparse_mat_l_name)

            # right
            sparse_mat_r_name='roi'+idroi_r+'_sparse_mat'
            sparse_mat_r = os.path.join(working_dir, subject,sparse_mat_r_name)
            
	        # get id of last voxel of fdt_matrix1.dot (it will be the length of the vector of connectivity of each voxel )
            fdt_mat_filepath = os.path.join(data_dir, subject,'fdt_matrix1.dot')
            line1 = subprocess.check_output(['tail','-1',fdt_mat_filepath])
            l = line1.split()
            length = int(l[0]) 

            # get output file name
            # left
            output_l_name='roi'+idroi_l+'_cc_mat'
            output_mat_l = os.path.join(working_dir, subject,output_l_name)
            # right
            output_r_name='roi'+idroi_r+'_cc_mat'
            output_mat_r = os.path.join(working_dir, subject,output_r_name)

            # compute correlation matrix
            # left
            compute_cc_mat(ids_roi_l, sparse_mat_l, length, output_mat_l) 
            # right
            compute_cc_mat(ids_roi_r, sparse_mat_r, length, output_mat_r) 
        
