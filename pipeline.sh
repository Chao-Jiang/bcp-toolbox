#! /bin/bash

# Brain Connectivity Parcellation toolbox
# pipeline file
# Ana Coelho

PIPELINE=$1
shift
WD=$1
shift 
DATA_DIR=$1
shift
SUBJ_LIST=$1
shift
ROI=$1
shift
MAX_CL_NUM=$1

# fetch the variables
set -o allexport

# create log directory 
#mkdir ${WD}/log

# create a folder for each subject in the working directory
for sub in `cat ${SUBJ_LIST}`
do
	#mkdir ${WD}/${sub}
	mkdir ${WD}/${sub}/${ROI}
done

ROI_ID_L=0
ROI_ID_R=0

# 0) get IDs of ROI
echo "=============== 0_get_roi_ids start! ===============" |tee -a ${WD}/log/progress_check.txt
T="$(date +%s)"
ids="$(python ${PIPELINE}/get_roi_ids.py ${PIPELINE} ${ROI})"
set -- $ids
ROI_ID_L=$1
ROI_ID_R=$2
#echo "${ROI_ID_L}"
#echo "${ROI_ID_R}"
#T="$(($(date +%s)-T))"
#echo "=============== 0_get_roi_ids done! ===============" |tee -a ${WD}/log/progress_check.txt
#printf "Time elapsed: %02d:%02d:%02d:%02d\n\n" "$((T/86400))" "$((T/3600%24))" "$((T/60%60))" "$((T%60))" |tee -a ${WD}/log/progress_check.txt
#
## 1) save voxel IDs of the ROI in a file 
#echo "=============== 1_group_id_roi start! ===============" |tee -a ${WD}/log/progress_check.txt
#T="$(date +%s)"
#python ${PIPELINE}/group_id_roi.py ${WD} ${DATA_DIR} ${SUBJ_LIST} ${ROI_ID_L} ${ROI_ID_R}
#T="$(($(date +%s)-T))"
#echo "$=============== 1_group_id_roi done! ===============" |tee -a ${WD}/log/progress_check.txt
#printf "Time elapsed: %02d:%02d:%02d:%02d\n\n" "$((T/86400))" "$((T/3600%24))" "$((T/60%60))" "$((T%60))" |tee -a ${WD}/log/progress_check.txt
#
## 2) get sparse connectivity matrix for ROI
#echo "=============== 2_get_connectivity_mat start! ===============" |tee -a ${WD}/log/progress_check.txt
#T="$(date +%s)"
#python ${PIPELINE}/get_connectivity_mat.py ${WD} ${DATA_DIR} ${SUBJ_LIST} ${ROI_ID_L} ${ROI_ID_R} # <----- add number of cores 
#T="$(($(date +%s)-T))"
#echo "=============== 2_get_connectivity_mat done! ===============" |tee -a ${WD}/log/progress_check.txt
#printf "Time elapsed: %02d:%02d:%02d:%02d\n\n" "$((T/86400))" "$((T/3600%24))" "$((T/60%60))" "$((T%60))" |tee -a ${WD}/log/progress_check.txt

# 3) compute correlation between each row of the sparse connectivity matrix and save to a new matrix
#echo "=============== 3_rows_correlation start! ===============" |tee -a ${WD}/log/progress_check.txt
#T="$(date +%s)"
#python ${PIPELINE}/rows_correlation.py ${WD} ${DATA_DIR} ${SUBJ_LIST} ${ROI_ID_L} ${ROI_ID_R}
#T="$(($(date +%s)-T))"
#echo "=============== 3_rows_correlation done! ===============" |tee -a ${WD}/log/progress_check.txt
#printf "Time elapsed: %02d:%02d:%02d:%02d\n\n" "$((T/86400))" "$((T/3600%24))" "$((T/60%60))" "$((T%60))" |tee -a ${WD}/log/progress_check.txt

# 4) apply hierarchical clustering to correlation matrix
echo "=============== 4_cluster_cc_mat start! ===============" |tee -a ${WD}/log/progress_check.txt
T="$(date +%s)"
python ${PIPELINE}/cluster_corr_mat.py ${WD} ${SUBJ_LIST} ${ROI_ID_L} ${ROI_ID_R}
T="$(($(date +%s)-T))"
echo "=============== 4_cluster_cc_mat done! ===============" |tee -a ${WD}/log/progress_check.txt
printf "Time elapsed: %02d:%02d:%02d:%02d\n\n" "$((T/86400))" "$((T/3600%24))" "$((T/60%60))" "$((T%60))" |tee -a ${WD}/log/progress_check.txt

# 5) get coordinates of each cluster and save to text file
echo "=============== 5_get_clusters start! ===============" |tee -a ${WD}/log/progress_check.txt
T="$(date +%s)"
python ${PIPELINE}/get_clusters.py ${WD} ${DATA_DIR} ${SUBJ_LIST} ${ROI} ${ROI_ID_L} ${ROI_ID_R} ${MAX_CL_NUM}
T="$(($(date +%s)-T))"
echo "=============== 5_get_clusters done! ===============" |tee -a ${WD}/log/progress_check.txt
printf "Time elapsed: %02d:%02d:%02d:%02d\n\n" "$((T/86400))" "$((T/3600%24))" "$((T/60%60))" "$((T%60))" |tee -a ${WD}/log/progress_check.txt

## 6) create image of the clusters from its coordinates and normalize to mni
#echo "=============== 6_create_mask_cluster start! ===============" |tee -a ${WD}/log/progress_check.txt
#T="$(date +%s)"
#bash ${PIPELINE}/create_mask_cluster.sh ${WD} ${DATA_DIR} ${SUBJ_LIST} ${ROI_ID_L} ${ROI_ID_R} ${MAX_CL_NUM}
#T="$(($(date +%s)-T))"
#echo "=============== 6_create_mask_cluster done! ===============" |tee -a ${WD}/log/progress_check.txt
#printf "Time elapsed: %02d:%02d:%02d:%02d\n\n" "$((T/86400))" "$((T/3600%24))" "$((T/60%60))" "$((T%60))" |tee -a ${WD}/log/progress_check.txt

## 7) create mpm 
#echo "=============== 7_create_mpm start! ===============" |tee -a ${WD}/log/progress_check.txt
#T="$(date +%s)"
#python ${PIPELINE}/create_mpm.py ${WD} ${DATA_DIR} ${SUBJ_LIST} ${ROI_ID_L} ${ROI_ID_R} ${MAX_CL_NUM}
#T="$(($(date +%s)-T))"
#echo "=============== 7_create_mpm done! ===============" |tee -a ${WD}/log/progress_check.txt
#printf "Time elapsed: %02d:%02d:%02d:%02d\n\n" "$((T/86400))" "$((T/3600%24))" "$((T/60%60))" "$((T%60))" |tee -a ${WD}/log/progress_check.txt

# 8) validation
#echo "=============== 8_validation start! ===============" |tee -a ${WD}/log/progress_check.txt
#T="$(date +%s)"
#python ${PIPELINE}/validation.py ${WD} ${DATA_DIR} ${SUBJ_LIST} ${ROI_ID_L} ${ROI_ID_R} ${MAX_CL_NUM}
#T="$(($(date +%s)-T))"
#echo "=============== 8_validation done! ===============" |tee -a ${WD}/log/progress_check.txt
#printf "Time elapsed: %02d:%02d:%02d:%02d\n\n" "$((T/86400))" "$((T/3600%24))" "$((T/60%60))" "$((T%60))" |tee -a ${WD}/log/progress_check.txt

echo "----------------All Done!!----------------"
