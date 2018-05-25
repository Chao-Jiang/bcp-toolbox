#!/usr/bin/env python

import os
import sys
import numpy as np
import nibabel as nib

def compute_mpm(image_4d):
	data = image_4d.get_data()
	size = data.shape
	mpm = np.zeros((size[0],size[1],size[2]))
	for i in xrange(size[0]):
		for j in xrange(size[1]):
			for k in xrange(size[2]):
				voxel=data[i][j][k]
				unique, counts = np.unique(voxel, return_counts=True)
				counts_dict = dict(zip(unique, counts))
				cl_max = max(counts_dict.keys(), key=(lambda k: counts_dict[k]))
				mpm[i][j][k] = cl_max

	return mpm


# check if we have all the arguments
if len(sys.argv) < 6:
	print 'usage: group_id_roi <working_dir> <data_dir> <subjects_file> <roi_id_l> <roi_id_r> <max_nr_clusters>'

else:
	# get directories
	working_dir = str(sys.argv[1])
	data_dir = str(sys.argv[2])

	# get roi ids (left and right)
	roi_id_l = int(sys.argv[4])
	roi_id_r = int(sys.argv[5])
	max_n_clusters=int(sys.argv[6])

	for i in xrange(2,max_n_clusters+1):

		# create list with path to cluster images of all subjects
		img_list_l=[]
		img_list_r=[]

		subjects_filepath = str(sys.argv[3])
		with open(subjects_filepath, 'r') as subjects:
			mylist = subjects.read().splitlines()
			for line in mylist:
				# get subject name from file
				subject=line

				# get path to cluster image
				cluster_file_l=os.path.join(working_dir,subject,'k'+str(i)+'_roi'+str(roi_id_l)+'_cluster_mni.nii.gz')
				cluster_file_r=os.path.join(working_dir,subject,'k'+str(i)+'_roi'+str(roi_id_r)+'_cluster_mni.nii.gz')
				# add to list of images
				img_list_l.append(cluster_file_l)
				img_list_r.append(cluster_file_r)
	
		#print (img_list_l)	
		all_img_l = nib.concat_images(img_list_l)
		all_img_r = nib.concat_images(img_list_r)

		# compute mpm and save to file
		# left
		mpm_l = compute_mpm(all_img_l)
		# get header of one cluster image to create a new image to mpm
		img = nib.load(img_list_l[0])
		mpm_img_l = nib.Nifti1Image(mpm_l, img.affine, img.header)
		nib.save(mpm_img_l, os.path.join(working_dir,'k'+str(i)+'_roi'+str(roi_id_l)+'mpm.nii.gz'))

		# right
		mpm_r = compute_mpm(all_img_r)
		mpm_img_r = nib.Nifti1Image(mpm_r, img.affine, img.header)
		nib.save(mpm_img_r, os.path.join(working_dir,'k'+str(i)+'_roi'+str(roi_id_r)+'mpm.nii.gz'))

		
		
