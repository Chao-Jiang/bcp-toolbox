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
    with open(fdt_mat_file, 'r') as sparse_mat:
         #for line in sparse_mat:
         for line in itertools.islice(sparse_mat, first_line, last_line):
             l = line.split()
             v_id1 = int(l[0])
             v_id2 = int(l[1])
             value = int(l[2])
             if v_id1 in ids_roi:
                 rows.append(line)
                 #with open(output_file, 'w') as out_file:
                 #    out_file.write(line)
                 #print(v_id1)
             elif v_id2 in ids_roi:
                 rows.append(line)
                 #with open(output_file, 'w') as out_file:
                 #    out_file.write(line)
                 #print(v_id2)

    #print coords
    #filename = 'sparse_mat_roi_40.txt'
    #out_file = os.path.join(directory, output_file)
    #np.savetxt(output_file,rows)
    #print filename

    #with open(output_file, 'wb') as fp:
    #    pickle.dump(rows, fp)
    with open(output_file, 'w') as of:
        of.writelines(rows)

# check if we have all the arguments
if len(sys.argv) < 3:
    print ('usage: get_connectivity_mat <subjects_file> <id_roi>')
else:
    directory_m1 = '/media/neuroimaging/TOSHIBA/SWBOX_probtrackx/M1/'
 
    # open subjects file
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
            ids_roi = loadtxt(ids_roi_filepath)
            #print ids_roi_filepath
            
            # get sparse voxel-wise connectivity matrix
            fdt_mat_filepath = os.path.join(directory_m1, subject,'fdt_matrix1.dot')
            #print fdt_mat_filepath
            
            # get number of lines in sparse matrix and compute increment to parallel computing
            length = file_len(fdt_mat_filepath)
            #print length
            increment = int(length / 6)
            #print increment
            
            # get ouptut file name
            output_file = os.path.join(directory_m1, subject, 'roi'+idroi+'_part')
            #print output_file
 
            # create the multiple processes to run in parallel
            Pros = []
            
            start_time = time.time()

            p = multiprocessing.Process(target=get_mat_lines, args=(directory_m1, ids_roi, fdt_mat_filepath, 0, increment, output_file+'1'))
            Pros.append(p)
            p.start()

            p = multiprocessing.Process(target=get_mat_lines, args=(directory_m1, ids_roi, fdt_mat_filepath, increment+1, increment*2, output_file+'2'))
            Pros.append(p)
            p.start()
            
            p = multiprocessing.Process(target=get_mat_lines, args=(directory_m1, ids_roi, fdt_mat_filepath, increment*2+1, increment*3, output_file+'3'))
            Pros.append(p)
            p.start()
            
            p = multiprocessing.Process(target=get_mat_lines, args=(directory_m1, ids_roi, fdt_mat_filepath, increment*3+1, increment*4, output_file+'4'))
            Pros.append(p)
            p.start()
            
            p = multiprocessing.Process(target=get_mat_lines, args=(directory_m1, ids_roi, fdt_mat_filepath, increment*4+1, increment*5, output_file+'5'))
            Pros.append(p)
            p.start()
            
            p = multiprocessing.Process(target=get_mat_lines, args=(directory_m1, ids_roi, fdt_mat_filepath, increment*5+1, length, output_file+'6'))
            Pros.append(p)
            p.start()
        # block until all the threads finish (i.e. block until all function_x calls finish)    
            for t in Pros:
                t.join()
            
            print("--- %s seconds ---" % (time.time() - start_time))

            # concatenate all the files created in a single sparse matrix
            listfiles = []
            listfiles.append(output_file+'1')   
            listfiles.append(output_file+'2')   
            listfiles.append(output_file+'3')   
            listfiles.append(output_file+'4')   
            listfiles.append(output_file+'5')   
            listfiles.append(output_file+'6')   
            
            out_sparse_file = os.path.join(directory_m1, subject, 'roi'+idroi+'_sparse_mat')
            concatenate_files(listfiles, out_sparse_file)


