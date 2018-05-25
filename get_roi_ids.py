#!/usr/bin/env python

import os
import sys
import numpy as np

def get_roi_ids(roi_name, match_file):
	with open(match_file, 'r') as match:
		for line in match:
			l=line.split()
			name= str(l[0])
			if name==roi_name:
				roi_l = int(l[1])
				roi_r = int(l[2])
				break

	return (roi_l,roi_r)


# check if we have all the arguments
if len(sys.argv) < 2:
    print ('usage: match_roi_name <pipeline> <roi_name>')
else:

	pipeline=str(sys.argv[1])
	roi_name=str(sys.argv[2])
	mfile=os.path.join(pipeline,'aal_names_ids.txt')
	(roi_id_l,roi_id_r)=get_roi_ids(roi_name,mfile)
	print roi_id_l  
	print roi_id_r