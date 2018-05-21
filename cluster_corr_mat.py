#!/usr/bin/env python

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import cophenet

def fancy_dendrogram(*args, **kwargs):
    max_d = kwargs.pop('max_d', None)
    if max_d and 'color_threshold' not in kwargs:
        kwargs['color_threshold'] = max_d
    annotate_above = kwargs.pop('annotate_above', 0)

    ddata = dendrogram(*args, **kwargs)

    if not kwargs.get('no_plot', False):
        plt.title('Hierarchical Clustering Dendrogram (truncated)')
        plt.xlabel('sample index or (cluster size)')
        plt.ylabel('distance')
        for i, d, c in zip(ddata['icoord'], ddata['dcoord'], ddata['color_list']):
            x = 0.5 * sum(i[1:3])
            y = d[1]
            if y > annotate_above:
                plt.plot(x, y, 'o', c=c)
                plt.annotate("%.3g" % y, (x, y), xytext=(0, -5),
                             textcoords='offset points',
                             va='top', ha='center')
        if max_d:
            plt.axhline(y=max_d, c='k')
    return ddata

def seriation(Z,N,cur_index):
    '''
        input:
            - Z is a hierarchical tree (dendrogram)
            - N is the number of points given to the clustering process
            - cur_index is the position in the tree for the recursive traversal
        output:
            - order implied by the hierarchical tree Z

        seriation computes the order implied by a hierarchical tree (dendrogram)
    '''
    if cur_index < N:
        return [cur_index]
    else:
        left = int(Z[cur_index-N,0])
        right = int(Z[cur_index-N,1])
        return (seriation(Z,N,left) + seriation(Z,N,right))

def compute_serial_matrix(dist_mat,method="ward"):
    '''
        input:
            - dist_mat is a distance matrix
            - method = ["ward","single","average","complete"]
        output:
            - seriated_dist is the input dist_mat,
              but with re-ordered rows and columns
              according to the seriation, i.e. the
              order implied by the hierarchical tree
            - res_order is the order implied by
              the hierarhical tree
            - res_linkage is the hierarhical tree (dendrogram)

        compute_serial_matrix transforms a distance matrix into
        a sorted distance matrix according to the order implied
        by the hierarchical tree (dendrogram)
    '''
    N = len(dist_mat)
    #flat_dist_mat = squareform(dist_mat)
    res_linkage = linkage(dist_mat, method=method)
    c, coph_dists = cophenet(res_linkage, pdist(dist_mat))
    print('Cophenetic correlation coeficient: {}'.format(c))
    res_order = seriation(res_linkage, N, N + N-2)
    seriated_dist = np.zeros((N,N))
    a,b = np.triu_indices(N,k=1)
    seriated_dist[a,b] = dist_mat[ [res_order[i] for i in a], [res_order[j] for j in b]]
    seriated_dist[b,a] = seriated_dist[a,b]

    return seriated_dist, res_order, res_linkage


#check if we have all arguments
if len(sys.argv) < 3:
    print ('usage: cluster_corr_mat <subjects_file> <id_roi>')
else:

    directory_m1 = '/media/neuroimaging/TOSHIBA/SWBOX_probtrackx/M1/'

    subjects_filepath = str(sys.argv[1])
    with open(subjects_filepath, 'r') as subjects:
        mylist = subjects.read().splitlines()
        for line in mylist:
            # get subject name from file
            subject = line+'_M1'
            print (subject)

            # get id of ROI and file with distance matrix
            idroi=str(sys.argv[2])
            dist_mat_name='roi'+idroi+'_cc_mat'
            dist_mat_filepath = os.path.join(directory_m1, subject, dist_mat_name)
            dist_mat = np.loadtxt(dist_mat_filepath)

	    # run hierarchical clustering
	    ordered_dist_mat, res_order, res_linkage = compute_serial_matrix(dist_mat,'average')
	    
	    # save ordered distance matrix
	    output_name='roi'+idroi+'_ordered_cc_mat'
            output_mat_file = os.path.join(directory_m1, subject, output_name)
	    np.savetxt(output_mat_file, ordered_dist_mat)

	    # save clustering results (merges order and distances)
	    results_name='roi'+idroi+'_results_linkage'
	    results_file = os.path.join(directory_m1, subject, results_name)
	    np.savetxt(results_file, res_linkage)

	    # save image of dendrogram
	    plt.figure(figsize=(25,10))
	    plt.title('Hierarchical Clustering Dendrogram')
	    plt.xlabel('voxel index')
	    plt.ylabel('distance')
	    dendrogram(res_linkage,leaf_rotation=90.,leaf_font_size=8.,)
	    dendrogram_name = 'roi'+idroi+'dendrogram.png'
	    dendrogram_file = os.path.join(directory_m1, subject, dendrogram_name)
	    plt.savefig(dendrogram_file)
