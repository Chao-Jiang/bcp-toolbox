#!/bin/bash
working_dir=$1
shift
data_dir=$1
shift
subj_list=$1
shift
roi_id_l=$1
shift
roi_id_r=$1
shift
max_nr_clusters=$1

# read subjects file
while read -r line
do
	subject=$line
	echo "$subject"	

	# create mask for all cluster solutions
	for ((i=2;i<=$max_nr_clusters;i++))
	do
		echo "Creating mask for cluster $i ..."
		# get file
		# left
		cluster_file_l="$working_dir"/"$subject"/k"$i"_roi"$roi_id_l"_clusters.txt
		# right
		cluster_file_r="$working_dir"/"$subject"/k"$i"_roi"$roi_id_r"_clusters.txt

		# create mask for left ROI
		string_add=''
		n=0
		#echo "Reading coordinates for left ROI..."
		while read -r coords_l
		do
			# get coordinates from file
			x=$(echo $coords_l | awk '{print $1}')
			y=$(echo $coords_l | awk '{print $2}')
			z=$(echo $coords_l | awk '{print $3}')
			cluster_value=$(echo $coords_l | awk '{print $4}')

			# create mask for each coordinate
			#fslmaths "$data_dir"/"$subject"/"$subject"_diff_b0_bet.nii.gz -mul 0 -add $cluster_value -roi $x 1 $y 1 $z 1 0 1 "$working_dir"/"$subject"/k"$i"_cluster_"$x"_"$y"_"$z".nii.gz -odt float
			if (( $(echo "$n" == "0" |bc -l) ));then 
				#string_add="$string_add "$working_dir"/"$subject"/k"$i"_cluster_"$x"_"$y"_"$z".nii.gz"
				fslmaths "$data_dir"/"$subject"/"$subject"_diff_b0_bet.nii.gz -mul 0 -add $cluster_value -roi $x 1 $y 1 $z 1 0 1 "$working_dir"/"$subject"/k"$i"_roi"$roi_id_l"_cluster_mask.nii.gz -odt float
			else
				#string_add="$string_add -add "$working_dir"/"$subject"/k"$i"_cluster_"$x"_"$y"_"$z".nii.gz"
				fslmaths "$data_dir"/"$subject"/"$subject"_diff_b0_bet.nii.gz -mul 0 -add $cluster_value -roi $x 1 $y 1 $z 1 0 1 "$working_dir"/"$subject"/k"$i"_cluster_"$x"_"$y"_"$z".nii.gz -odt float
				fslmaths "$working_dir"/"$subject"/k"$i"_roi"$roi_id_l"_cluster_mask.nii.gz  -add "$working_dir"/"$subject"/k"$i"_cluster_"$x"_"$y"_"$z".nii.gz "$working_dir"/"$subject"/k"$i"_roi"$roi_id_l"_cluster_mask.nii.gz 
				rm -f "$working_dir"/"$subject"/k"$i"_cluster_"$x"_"$y"_"$z".nii.gz
			fi
			n=$((n+1))

		done < "$cluster_file_l"

		#echo "Finished reading coordinates"

		# add all masks and remove old files
		#echo "Creating mask for left ROI ..."
		#fslmaths $string_add "$working_dir"/"$subject"/k"$i"_roi"$roi_id_l"_cluster_mask.nii.gz 
		#rm -f "$working_dir"/"$subject"/k"$i"_cluster_*
		#echo "Finished creating mask"

		# register to MNI
		#echo "Normalizing left mask to MNI space ..."
		flirt -in "$data_dir"/"$subject"/"$subject"_diff_b0_bet.nii.gz -ref /usr/local/fsl/data/standard/MNI152_T1_2mm_brain.nii.gz -omat "$working_dir"/"$subject"/diff2mni.mat #just need to do this the first time 
		flirt -interp nearestneighbour -in "$working_dir"/"$subject"/k"$i"_roi"$roi_id_l"_cluster_mask.nii.gz -ref /usr/local/fsl/data/standard/MNI152_T1_2mm_brain.nii.gz -applyxfm -init "$working_dir"/"$subject"/diff2mni.mat -out "$working_dir"/"$subject"/k"$i"_roi"$roi_id_l"_cluster_mni.nii.gz
		#echo "Finished normalization!"

		# -----------------//-----------------
		# create mask for right ROI
		string_add=''
		n=0
		#echo "Reading coordinates for right ROI..."
		while read -r coords_r
		do
			# get coordinates from file
			x=$(echo $coords_r | awk '{print $1}')
			y=$(echo $coords_r | awk '{print $2}')
			z=$(echo $coords_r | awk '{print $3}')
			cluster_value=$(echo $coords_r | awk '{print $4}')

			# create mask for each coordinate
			#fslmaths "$data_dir"/"$subject"/"$subject"_diff_b0_bet.nii.gz -mul 0 -add $cluster_value -roi $x 1 $y 1 $z 1 0 1 "$working_dir"/"$subject"/k"$i"_cluster_"$x"_"$y"_"$z".nii.gz -odt float
			if (( $(echo "$n" == "0" |bc -l) ));then 
				#string_add="$string_add "$working_dir"/"$subject"/k"$i"_cluster_"$x"_"$y"_"$z".nii.gz"
				fslmaths "$data_dir"/"$subject"/"$subject"_diff_b0_bet.nii.gz -mul 0 -add $cluster_value -roi $x 1 $y 1 $z 1 0 1 "$working_dir"/"$subject"/k"$i"_roi"$roi_id_r"_cluster_mask.nii.gz  -odt float
			else
				#string_add="$string_add -add "$working_dir"/"$subject"/k"$i"_cluster_"$x"_"$y"_"$z".nii.gz"
				fslmaths "$data_dir"/"$subject"/"$subject"_diff_b0_bet.nii.gz -mul 0 -add $cluster_value -roi $x 1 $y 1 $z 1 0 1 "$working_dir"/"$subject"/k"$i"_cluster_"$x"_"$y"_"$z".nii.gz -odt float
				fslmaths "$working_dir"/"$subject"/k"$i"_roi"$roi_id_r"_cluster_mask.nii.gz  -add "$working_dir"/"$subject"/k"$i"_cluster_"$x"_"$y"_"$z".nii.gz "$working_dir"/"$subject"/k"$i"_roi"$roi_id_r"_cluster_mask.nii.gz
				rm -f "$working_dir"/"$subject"/k"$i"_cluster_"$x"_"$y"_"$z".nii.gz
			fi
			n=$((n+1))

		done < "$cluster_file_r"

		#echo "Finished reading coordinates"

		# add all masks and remove old files
		#echo "Creating mask for right ROI ..."
		#fslmaths $string_add "$working_dir"/"$subject"/k"$i"_roi"$roi_id_r"_cluster_mask.nii.gz 
		#rm -f "$working_dir"/"$subject"/k"$i"_cluster_*
		#echo "Finished creating mask"

		# register to MNI
		#echo "Normalizing right mask to MNI space ..."
		flirt -interp nearestneighbour -in "$working_dir"/"$subject"/k"$i"_roi"$roi_id_r"_cluster_mask.nii.gz -ref /usr/local/fsl/data/standard/MNI152_T1_2mm_brain.nii.gz -applyxfm -init "$working_dir"/"$subject"/diff2mni.mat -out "$working_dir"/"$subject"/k"$i"_roi"$roi_id_r"_cluster_mni.nii.gz
		#echo "Finished normalization!"
		echo "Done mask for cluster $i"

	done

done < "$subj_list"