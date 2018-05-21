#!/bin/bash

DIR="/media/neuroimaging/TOSHIBA/SWBOX_probtrackx"
filename=$1

while read -r line
do
	echo $line
	SUJ=$line
	./create_mask_cluster.sh $SUJ 1 36 hippocampus 2
	./create_mask_cluster.sh $SUJ 2 36 hippocampus 2
        ./create_mask_cluster.sh $SUJ 1 37 hippocampus 2
        ./create_mask_cluster.sh $SUJ 2 37 hippocampus 2

        ./create_mask_cluster.sh $SUJ 1 36 hippocampus 4
        ./create_mask_cluster.sh $SUJ 2 36 hippocampus 4
        ./create_mask_cluster.sh $SUJ 3 36 hippocampus 4
        ./create_mask_cluster.sh $SUJ 4 36 hippocampus 4
        ./create_mask_cluster.sh $SUJ 1 37 hippocampus 4
        ./create_mask_cluster.sh $SUJ 2 37 hippocampus 4
        ./create_mask_cluster.sh $SUJ 3 37 hippocampus 4
        ./create_mask_cluster.sh $SUJ 4 37 hippocampus 4

        ./create_mask_cluster.sh $SUJ 1 36 hippocampus 5
        ./create_mask_cluster.sh $SUJ 2 36 hippocampus 5
        ./create_mask_cluster.sh $SUJ 3 36 hippocampus 5
        ./create_mask_cluster.sh $SUJ 4 36 hippocampus 5
	./create_mask_cluster.sh $SUJ 5 36 hippocampus 5
        ./create_mask_cluster.sh $SUJ 1 37 hippocampus 5
        ./create_mask_cluster.sh $SUJ 2 37 hippocampus 5
        ./create_mask_cluster.sh $SUJ 3 37 hippocampus 5
        ./create_mask_cluster.sh $SUJ 4 37 hippocampus 5
	./create_mask_cluster.sh $SUJ 5 37 hippocampus 5

done < $filename
