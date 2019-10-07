#!/bin/sh

function help () {
echo "las2xyz - A simple script that converts all .laz files in a directory to .xyz files for a provided classification in a Region of Interest (ROI). Also outputs list of .laz files inside ROI (inbounds_datalist.txt) and outside ROI (outbounds_datalist.txt)."
	echo "Usage: $0 class roi_minx roi_miny roi_maxx roi_maxy"
	echo "* class: <the desired lidar return>
	0 Never classified
	1 Unassigned
	2 Ground
	3 Low Vegetation
	4 Medium Vegetation
	5 High Vegetation
	6 Building
	7 Low Point
	8 Reserved
	9 Water
	10 Rail
	11 Road Surface
	12 Reserved
	13 Wire - Guard (Shield)
	14 Wire - Conductor (Phase)
	15 Transmission Tower
	16 Wire-Structure Connector (Insulator)
	17 Bridge Deck
	18 High Noise"
	echo "* roi_minx: <min x-coordinate of ROI>"
	echo "* roi_miny: <min y-coordinate of ROI>"
	echo "* roi_maxx: <max x-coordinate of ROI>"
	echo "* roi_maxy: <max y-coordinate of ROI>"
}

total_files=$(ls -1 | grep '\.laz$' | wc -l)
echo "Total number of laz files to process:" $total_files

file_num=1

#see if 5 parameters were provided
#show help if not
if [ ${#@} == 5 ]; 
then
	#Create empty text files
	> inbounds_datalist.txt
	> outbounds_datalist.txt
	
	#User inputs    	
	class=$1
	roi_minx=$2
	roi_miny=$3
	roi_maxx=$4
	roi_maxy=$5

	for i in *.laz;
	do
		#Create tmp text file of lasinfo for each lidar file
		echo "Processing File" $file_num "out of" $total_files
		echo "Processing" $i
		lasinfo $i -stdout > lasinfo_tmp.txt
	
		#Get minx, maxx, miny, maxy from temporary file
		minx="$(grep -e "min x" lasinfo_tmp.txt | awk '{print $5}')"
		maxx="$(grep -e "max x" lasinfo_tmp.txt | awk '{print $5}')"
		miny="$(grep -e "min x" lasinfo_tmp.txt | awk '{print $6}')"
		maxy="$(grep -e "max x" lasinfo_tmp.txt | awk '{print $6}')"
			
		#see if its in bounds, make xyz
		if ((((((( $(echo "${maxx} <= $roi_maxx" |bc) ))) && ((( $(echo "${maxx} >= $roi_minx" |bc) )))) || (((( $(echo "${minx} <= $roi_maxx" |bc) ))) && ((( $(echo "${minx} >= $roi_minx" |bc) ))))) && ((((( $(echo "${maxy} <= $roi_maxy" |bc) ))) && ((( $(echo "${maxy} >= $roi_miny" |bc) )))) || (((( $(echo "${miny} <= $roi_maxy" |bc) ))) && ((( $(echo "${miny} >= $roi_miny" |bc) )))))))
		then
			ls $i >> "inbounds_datalist.txt"
			echo "$i in ROI; converting to xyz..."
			las2txt -i $i -keep_class $class -o $(basename $i .laz)"_class_"$class.xyz -parse xyz
		else
			ls $i >> "outbounds_datalist.txt"
			echo "$i outside ROI; ignored."
		fi
	file_num=$((file_num + 1))
	rm lasinfo_tmp.txt
	done

else
	help

fi





