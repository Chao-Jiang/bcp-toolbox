#!/usr/bin/env python

import os
import sys
import numpy as np 
from numpy import loadtxt

def get_ids_roi(directory, subject_name, coords_mat, roi_id):
	ids = coords_mat[np.ix_(coords_mat[:,3] == roi_id, np.array([False, False, False, False, True]))]
	#print coords
	filename = 'ids_roi' + str(roi_id) +'.txt'
	#roi_folder='roi'+str(roi_id)
	out_file = os.path.join(directory, subject_name,filename)
	np.savetxt(out_file,ids,fmt='%d')
	#print filename


# check if we have all the arguments
if len(sys.argv) < 6:
	print 'usage: group_id_roi <working_dir> <data_dir> <subjects_file> <roi_id_l> <roi_id_r>'

else:

	# get directories
	working_dir = str(sys.argv[1])
	data_dir = str(sys.argv[2])

	# get roi ids (left and right)
	roi_id_l = int(sys.argv[4])
	roi_id_r = int(sys.argv[5])

	subjects_filepath = str(sys.argv[3])
	with open(subjects_filepath, 'r') as subjects:
		mylist = subjects.read().splitlines()
		for line in mylist:
			# get subject name from file
			subject=line

			#get the input coords file
			coords_file = os.path.join(data_dir, subject, 'coords_for_fdt_matrix1')
			coords_mat = loadtxt(coords_file)

			#save coords of each ROI in a file
			get_ids_roi(working_dir, subject, coords_mat, roi_id_l)
			get_ids_roi(working_dir, subject, coords_mat, roi_id_r)

			print(subject+' done!')
			

