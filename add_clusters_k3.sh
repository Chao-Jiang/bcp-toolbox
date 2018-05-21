#!/bin/bash

DIR=/media/neuroimaging/TOSHIBA/SWBOX_probtrackx/M1
filename=$1
roi_id=$2

while read -r line
do
        echo $line
        SUJ=$line
	fslmaths "$DIR"/"$SUJ"_M1/roi"$roi_id"_cluster1_mni.nii.gz -add "$DIR"/"$SUJ"_M1/roi"$roi_id"_cluster2_mni.nii.gz -add "$DIR"/"$SUJ"_M1/roi"$roi_id"_cluster3_mni.nii.gz "$DIR"/"$SUJ"_M1/roi"$roi_id"_cluster_mni.nii.gz

done < "$filename"

