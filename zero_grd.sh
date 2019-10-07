#!/bin/sh

function help () {
echo "zero_grd- Script that creates a zero grid from a provided two-line xyz file of bounding box with zero elevations, at a provided cell size. The resulting zero grid is then converted back to xyz for input into VDatum to create a conversion grid."
	echo "Usage: $0 bb_zero_xyz cellsize "
	echo "* bb_zero_xyz file with zero elevation values"
	echo "* cellsize: <cell size in arc-seconds>
	0.1111111s/0.1111111s = 1/9th arc-second 
	0.3333333s/0.3333333s = 1/3rd arc-second
	1s/1s = 1 arc-second
	3s/3s = 3 arc-second"
}

#see if 2 parameters were provided
#show help if not
if [ ${#@} == 2 ]; 
then
	#User inputs 
	bb_zero_xyz=$1   	
	cellsize=$2

	#Get minx, maxx, miny, maxy from temporary file
	minx="$(gmt gmtinfo  $bb_zero_xyz -C | awk '{print $1}')"
	maxx="$(gmt gmtinfo  $bb_zero_xyz -C | awk '{print $2}')"
	miny="$(gmt gmtinfo  $bb_zero_xyz -C | awk '{print $3}')"
	maxy="$(gmt gmtinfo  $bb_zero_xyz -C | awk '{print $4}')"
	#short_name = 

	echo "minx is $minx"
	echo "maxx is $maxx"
	echo "miny is $miny"
	echo "maxy is $maxy"

	echo "coverting $bb_zero_xyz to zero grid..."
	gmt surface $bb_zero_xyz -R${minx}/${maxx}/${miny}/${maxy}  -G$(basename $bb_zero_xyz .xyz).tif=gd:GTiff -I$cellsize

	echo "coverting $bb_zero_xyz zero grid to xyz..."
	gmt grd2xyz $(basename $bb_zero_xyz .xyz).tif | tr "\\t" "," > $(basename $bb_zero_xyz .xyz)"_zeroes.xyz"

else
	help

fi































