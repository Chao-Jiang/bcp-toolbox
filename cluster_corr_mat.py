#!/usr/bin/env python

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import cophenet
import scipy.io as sio

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
if len(sys.argv) < 5:
    print ('usage: cluster_corr_mat <working_dir> <subjects_file> <id_roi_l> <id_roi_r>')
else:

    # get directories
    working_dir = str(sys.argv[1])

    subjects_filepath = str(sys.argv[2])
    with open(subjects_filepath, 'r') as subjects:
        mylist = subjects.read().splitlines()
        for line in mylist:
            # get subject name from file
            subject = line
            print (subject)

            # get id of ROI and correlation matrix
            # left
            idroi_l=str(sys.argv[3])
            cc_mat_l_name='roi'+idroi_l+'_cc_mat.mat'
            cc_mat_l_filepath = os.path.join(working_dir, subject, cc_mat_l_name)

            # load .mat file and convert to numpy array
            mat_contents_l = sio.loadmat(cc_mat_l_filepath)
            mat_l = mat_contents_l['cc_mat']
            cc_mat_l = np.array(mat_l)
            cc_mat_l[np.isnan(cc_mat_l)] = 0

            #cc_mat_l = np.loadtxt(cc_mat_l_filepath)

            # right
            idroi_r=str(sys.argv[4])
            cc_mat_r_name='roi'+idroi_r+'_cc_mat.mat'
            cc_mat_r_filepath = os.path.join(working_dir, subject, cc_mat_r_name)

            # load .mat file and convert to numpy array
            mat_contents_r = sio.loadmat(cc_mat_r_filepath)
            mat_r = mat_contents_r['cc_mat']
            cc_mat_r = np.array(mat_r)
            cc_mat_r[np.isnan(cc_mat_r)] = 0

            #cc_mat_r = np.loadtxt(cc_mat_r_filepath)

            # run hierarchical clustering
            # left
            ordered_dist_l_mat, res_order_l, res_linkage_l = compute_serial_matrix(cc_mat_l,'average')
            # right
            ordered_dist_r_mat, res_order_r, res_linkage_r = compute_serial_matrix(cc_mat_r,'average')

            # save ordered correlation matrix
            # left
            output_l_name='roi'+idroi_l+'_ordered_cc_mat'
            output_mat_l_file = os.path.join(working_dir, subject, output_l_name)
            np.savetxt(output_mat_l_file, ordered_dist_l_mat)

            # right
            output_r_name='roi'+idroi_r+'_ordered_cc_mat'
            output_mat_r_file = os.path.join(working_dir, subject, output_r_name)
            np.savetxt(output_mat_r_file, ordered_dist_r_mat)

            # save clustering results (merges order and distances)
            # left
            results_l_name='roi'+idroi_l+'_results_linkage'
            results_l_file = os.path.join(working_dir, subject, results_l_name)
            np.savetxt(results_l_file, res_linkage_l)

            #right
            results_r_name='roi'+idroi_r+'_results_linkage'
            results_r_file = os.path.join(working_dir, subject, results_r_name)
            np.savetxt(results_r_file, res_linkage_r)

            # save image of dendrogram
            # left
            plt.figure(figsize=(25,10))
            plt.title('Hierarchical Clustering Dendrogram')
            plt.xlabel('voxel index')
            plt.ylabel('distance')
            dendrogram(res_linkage_l,leaf_rotation=90.,leaf_font_size=8.,)
            dendrogram_l_name = 'roi'+idroi_l+'dendrogram.png'
            dendrogram_l_file = os.path.join(working_dir, subject, dendrogram_l_name)
            plt.savefig(dendrogram_l_file)

            # right
            plt.figure(figsize=(25,10))
            plt.title('Hierarchical Clustering Dendrogram')
            plt.xlabel('voxel index')
            plt.ylabel('distance')
            dendrogram(res_linkage_r,leaf_rotation=90.,leaf_font_size=8.,)
            dendrogram_r_name = 'roi'+idroi_r+'dendrogram.png'
            dendrogram_r_file = os.path.join(working_dir, subject, dendrogram_r_name)
            plt.savefig(dendrogram_r_file)
