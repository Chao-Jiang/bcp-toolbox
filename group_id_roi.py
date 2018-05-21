#!/usr/bin/env python

import os
import sys
import numpy as np 
from numpy import loadtxt

def get_ids_roi(directory, subject_name, coords_mat, roi_id):
	ids = coords_mat[np.ix_(coords_mat[:,3] == roi_id, np.array([False, False, False, False, True]))]
	#print coords
	filename = 'ids_roi' + str(roi_id) +'.txt'
	roi_folder='roi'+str(roi_id)
	out_file = os.path.join(directory, subject_name, roi_folder,filename)
	np.savetxt(out_file,ids,fmt='%d')
	print filename


# check if we have all the arguments
if len(sys.argv) < 3:
	print 'usage: group_id_roi <subjects_file> <roi_id>'

else:

	directory_m1 = '/Volumes/TOSHIBA/SWBOX_probtrackx/M1/'
	#directory_m2 = '/Volumes/TOSHIBA/SWBOX_probtrackx/M2/'
	roi_id = int(sys.argv[2])

	subjects_filepath = os.path.join('/Volumes/TOSHIBA/SWBOX_probtrackx/scripts/', str(sys.argv[1]))
	with open(subjects_filepath, 'r') as subjects:
		mylist = subjects.read().splitlines()
		for line in mylist:
			# get subject name from file
			subject = line
			print subject

			subject_m1  = subject + '_M1'
			#subject_m2  = subject + '_M2'

			#get the input coords file
			coords_file_m1 = os.path.join(directory_m1, subject_m1, 'coords_for_fdt_matrix1')
			coords_mat_m1 = loadtxt(coords_file_m1)
			#coords_file_m2 = os.path.join(directory_m2, subject_m2, 'coords_for_fdt_matrix1')
			#coords_mat_m2 = loadtxt(coords_file_m2)

			#save coords of each ROI in a file
			get_ids_roi(directory_m1, subject_m1, coords_mat_m1, roi_id)
			#save_coords(directory_m2, subject_m2, coords_mat_m2)

