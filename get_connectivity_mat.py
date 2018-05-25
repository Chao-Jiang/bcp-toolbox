#!/usr/bin/env python

import os
import sys
import time
import numpy as np 
from numpy import loadtxt
from numpy import savetxt
import itertools
import pickle
import subprocess
import multiprocessing


def concatenate_files(list_files, output_file):
	with open(output_file, 'w') as outfile:
		for file in list_files:
			with open(file) as infile:
				for line in infile:
					outfile.write(line)
                    
def file_len(fname):
    p = subprocess.Popen(['wc', '-l', fname], stdout=subprocess.PIPE, 
                                              stderr=subprocess.PIPE)
    result, err = p.communicate()
    if p.returncode != 0:
        raise IOError(err)
    return int(result.strip().split()[0])

def get_mat_lines(directory, ids_roi, fdt_mat_file, first_line, last_line, output_file):

    rows = []
    # get lines of whole sparse matrix that correspond to the ROI
    with open(fdt_mat_file, 'r') as sparse_mat:
         for line in itertools.islice(sparse_mat, first_line, last_line):
             l = line.split()
             v_id1 = int(l[0])
             v_id2 = int(l[1])
             value = int(l[2])
             if v_id1 in ids_roi:
                 rows.append(line)
             elif v_id2 in ids_roi:
                 rows.append(line)

    with open(output_file, 'w') as of:
        of.writelines(rows)

# check if we have all the arguments
if len(sys.argv) < 6:
    print ('usage: get_connectivity_mat <working_dir> <data_dir> <subjects_file> <id_roi_l> <id_roi_r>')
else:
    # get directories
    working_dir = str(sys.argv[1])
    data_dir = str(sys.argv[2])
 
    # open subjects file
    subjects_filepath = str(sys.argv[3])
    with open(subjects_filepath, 'r') as subjects:
        mylist = subjects.read().splitlines()
        for line in mylist:
            # get subject name from file
            subject = line
            #print (subject)
            
            # get ids of ROI and file with voxel ids 
            # left
            idroi_l=str(sys.argv[4])
            id_roi_l_name='ids_roi'+idroi_l+'.txt'
            ids_roi_l_filepath = os.path.join(working_dir, subject,id_roi_l_name)
            ids_roi_l = loadtxt(ids_roi_l_filepath)

            # right
            idroi_r=str(sys.argv[5])
            id_roi_r_name='ids_roi'+idroi_r+'.txt'
            ids_roi_r_filepath = os.path.join(working_dir, subject,id_roi_r_name)
            ids_roi_r = loadtxt(ids_roi_r_filepath)
            
            # get sparse voxel-wise connectivity matrix
            fdt_mat_filepath = os.path.join(data_dir, subject,'fdt_matrix1.dot')
            
            # get number of lines in sparse matrix and compute increment to parallel computing
            length = file_len(fdt_mat_filepath)
            increment = int(length / 6)
            
            # get ouptut file names
            output_file_l = os.path.join(working_dir, subject, 'roi'+idroi_l+'_part')
            output_file_r = os.path.join(working_dir, subject, 'roi'+idroi_r+'_part')
 
            # create the multiple processes to run in parallel
            # left
            Pros_l = []
            
            start_time = time.time()

            p = multiprocessing.Process(target=get_mat_lines, args=(data_dir, ids_roi_l, fdt_mat_filepath, 0, increment, output_file_l+'1'))
            Pros_l.append(p)
            p.start()

            p = multiprocessing.Process(target=get_mat_lines, args=(data_dir, ids_roi_l, fdt_mat_filepath, increment+1, increment*2, output_file_l+'2'))
            Pros_l.append(p)
            p.start()
            
            p = multiprocessing.Process(target=get_mat_lines, args=(data_dir, ids_roi_l, fdt_mat_filepath, increment*2+1, increment*3, output_file_l+'3'))
            Pros_l.append(p)
            p.start()
            
            p = multiprocessing.Process(target=get_mat_lines, args=(data_dir, ids_roi_l, fdt_mat_filepath, increment*3+1, increment*4, output_file_l+'4'))
            Pros_l.append(p)
            p.start()
            
            p = multiprocessing.Process(target=get_mat_lines, args=(data_dir, ids_roi_l, fdt_mat_filepath, increment*4+1, increment*5, output_file_l+'5'))
            Pros_l.append(p)
            p.start()
            
            p = multiprocessing.Process(target=get_mat_lines, args=(data_dir, ids_roi_l, fdt_mat_filepath, increment*5+1, length, output_file_l+'6'))
            Pros_l.append(p)
            p.start()
            # block until all the threads finish (i.e. block until all function_x calls finish)    
            for t in Pros_l:
                t.join()
            
            print("--- %s seconds ---" % (time.time() - start_time))

            # right
            Pros_r = []
            
            start_time = time.time()

            p = multiprocessing.Process(target=get_mat_lines, args=(data_dir, ids_roi_r, fdt_mat_filepath, 0, increment, output_file_r+'1'))
            Pros_r.append(p)
            p.start()

            p = multiprocessing.Process(target=get_mat_lines, args=(data_dir, ids_roi_r, fdt_mat_filepath, increment+1, increment*2, output_file_r+'2'))
            Pros_r.append(p)
            p.start()
            
            p = multiprocessing.Process(target=get_mat_lines, args=(data_dir, ids_roi_r, fdt_mat_filepath, increment*2+1, increment*3, output_file_r+'3'))
            Pros_r.append(p)
            p.start()
            
            p = multiprocessing.Process(target=get_mat_lines, args=(data_dir, ids_roi_r, fdt_mat_filepath, increment*3+1, increment*4, output_file_r+'4'))
            Pros_r.append(p)
            p.start()
            
            p = multiprocessing.Process(target=get_mat_lines, args=(data_dir, ids_roi_r, fdt_mat_filepath, increment*4+1, increment*5, output_file_r+'5'))
            Pros_r.append(p)
            p.start()
            
            p = multiprocessing.Process(target=get_mat_lines, args=(data_dir, ids_roi_r, fdt_mat_filepath, increment*5+1, length, output_file_r+'6'))
            Pros_r.append(p)
            p.start()
            # block until all the threads finish (i.e. block until all function_x calls finish)    
            for t in Pros_r:
                t.join()
            
            print("--- %s seconds ---" % (time.time() - start_time))

            # concatenate all the files created in a single sparse matrix
            # left 
            listfiles_l = []
            listfiles_l.append(output_file_l+'1')   
            listfiles_l.append(output_file_l+'2')   
            listfiles_l.append(output_file_l+'3')   
            listfiles_l.append(output_file_l+'4')   
            listfiles_l.append(output_file_l+'5')   
            listfiles_l.append(output_file_l+'6')   
            
            out_sparse_file_l = os.path.join(working_dir, subject, 'roi'+idroi_l+'_sparse_mat')
            concatenate_files(listfiles_l, out_sparse_file_l)

            # delete part files
            for file in listfiles_l:
                try:
                    os.remove(file)
                except OSError, e:  ## if failed, report it back to the user ##
                    print ("Error: %s - %s." % (e.filename,e.strerror))

            # right 
            listfiles_r = []
            listfiles_r.append(output_file_r+'1')   
            listfiles_r.append(output_file_r+'2')   
            listfiles_r.append(output_file_r+'3')   
            listfiles_r.append(output_file_r+'4')   
            listfiles_r.append(output_file_r+'5')   
            listfiles_r.append(output_file_r+'6')   
            
            out_sparse_file_r = os.path.join(working_dir, subject, 'roi'+idroi_r+'_sparse_mat')
            concatenate_files(listfiles_r, out_sparse_file_r)

            # delete part files
            for file in listfiles_r:
                try:
                    os.remove(file)
                except OSError, e:  ## if failed, report it back to the user ##
                    print ("Error: %s - %s." % (e.filename,e.strerror))

