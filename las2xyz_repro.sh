#!/bin/sh

function help () {
echo "las2xyz_repro - A simple script that converts all .las files in a directory from projected coords to geographic coords and then to xyz files for a provided classification"
	echo "Usage: $0 class input_epsg input_vert_units output_vert_units"
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
	echo "* input_epsg: <the input epsg code>"
	echo "* input_vert_units: <the input vertical units, ie, feet or meter>"
	echo "* output_vert_units: <the output vertical units, ie, feet or meter>"
}

total_files=$(ls -1 | grep '\.las$' | wc -l)
echo "Total number of las files to process:" $total_files

file_num=1

#see if 4 parameters were provided
#show help if not
if [ ${#@} == 4 ]; 
then
	mkdir -p xyz
	#User inputs    	
	class=$1
	input_epsg=$2
	input_vert_units=$3
	output_vert_units=$4

	for i in *.las;
	do
		echo "Processing File" $file_num "out of" $total_files
		echo "Reprojecting:" $i
		las2las -i $i -o $(basename $i .las)"_nad83.las" -epsg $input_epsg "-elevation_"$input_vert_units -target_longlat -nad83 "-target_"$output_vert_units
		echo "Converting to xyz:" $i
		las2txt -i $(basename $i .las)"_nad83.las" -keep_class $class -o xyz/$(basename $i .las)"_class_"$class.xyz -parse xyz
		rm $(basename $i .las)"_nad83.las"
		file_num=$((file_num + 1))
	done
else
	help

fi
