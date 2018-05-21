#!/bin/bash
DIR=/media/neuroimaging/TOSHIBA/SWBOX_probtrackx/M1

filename="$1"
roi_id="$2"
roi_name="$3"
n_clusters="$4"

while read -r line
do
	SUJ="$line"
	echo $SUJ
	#flirt -in "$DIR"/"$SUJ"_M1/"$SUJ"_diff_b0_bet.nii.gz -ref /usr/local/fsl/data/standard/MNI152_T1_2mm_brain.nii.gz -omat "$DIR"/"$SUJ"_M1/diff2mni.mat
	for ((i=1; i<=$n_clusters; i++))
	do
		flirt -interp nearestneighbour -in "$DIR"/"$SUJ"_M1/"$roi_name"/k"$n_clusters"/roi"$roi_id"_cluster"$i"_mask.nii.gz -ref /usr/local/fsl/data/standard/MNI152_T1_2mm_brain.nii.gz -applyxfm -init "$DIR"/"$SUJ"_M1/diff2mni.mat -out "$DIR"/"$SUJ"_M1/"$roi_name"/k"$n_clusters"/roi"$roi_id"_cluster"$i"_mni.nii.gz
	done

done < "$filename"
