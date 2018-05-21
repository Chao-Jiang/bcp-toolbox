#!/bin/bash

DIR="/media/neuroimaging/TOSHIBA/SWBOX_probtrackx"

#filename="$1"
SUJ="$1"
cluster_id="$2"
roi_id="$3"
roi_name="$4"
n_clusters="$5"
#cat $filename | while read x y z; do echo $x -- $y -- $z; done

string_add=''
n=0
filename="$DIR"/M1/"$SUJ"_M1/"$roi_name"/k"$n_clusters"/roi"$roi_id"_cluster"$cluster_id".txt
#echo $filename

echo "Reading coordinates..."
while read -r line
do
	# get coordinates from file
	x=$(echo $line | awk '{print $1}')
	y=$(echo $line | awk '{print $2}')
	z=$(echo $line | awk '{print $3}')

	#echo $x $y $z

	# create mask for each coordinate
	fslmaths "$DIR"/M1/"$SUJ"_M1/"$SUJ"_diff_b0_bet.nii.gz -mul 0 -add $cluster_id -roi $x 1 $y 1 $z 1 0 1 "$DIR"/M1/"$SUJ"_M1/"$roi_name"/k"$n_clusters"/cluster"$cluster_id"_"$x"_"$y"_"$z".nii.gz -odt float
	if (( $(echo "$n" == "0" |bc -l) ));then 
		string_add="$string_add "$DIR"/M1/"$SUJ"_M1/"$roi_name"/k"$n_clusters"/cluster"$cluster_id"_"$x"_"$y"_"$z".nii.gz"
	else
		string_add="$string_add -add "$DIR"/M1/"$SUJ"_M1/"$roi_name"/k"$n_clusters"/cluster"$cluster_id"_"$x"_"$y"_"$z".nii.gz"
	fi
	n=$((n+1))
done < "$filename"

echo "Finished reading coordinates"
#echo $string_add

# add all masks and remove old files
echo "Creating mask..."
fslmaths $string_add "$DIR"/M1/"$SUJ"_M1/"$roi_name"/k"$n_clusters"/roi"$roi_id"_cluster"$cluster_id"_mask.nii.gz 
rm -f "$DIR"/M1/"$SUJ"_M1/"$roi_name"/k"$n_clusters"/cluster"$cluster_id"_*
echo "Finished creating mask"
