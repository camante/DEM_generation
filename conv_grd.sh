#!/bin/sh


function help () {
echo "conv_grd - Creates a conversion grd from vdatum xyz points for a provided cell size and constrains results to minmax of input xyz"
	echo "Usage: $input $0 cellsize"
	echo "* input_xyz: <input xyz file>"
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
	input_xyz=$1
	cellsize=$2

	echo "Geting minx, maxx, miny, maxy, minz, maxz from input file"
	gmt gmtinfo $input_xyz -C > minmax.txt

	minx="$(head minmax.txt | awk '{print $1}')"
	maxx="$(head minmax.txt | awk '{print $2}')"
	miny="$(head minmax.txt | awk '{print $3}')"
	maxy="$(head minmax.txt | awk '{print $4}')"
	minz="$(head minmax.txt | awk '{print $5}')"
	maxz="$(head minmax.txt | awk '{print $6}')"

	echo "minx is $minx"
	echo "maxx is $maxx"
	echo "miny is $miny"
	echo "maxy is $maxy"
	echo "minz is $minz"
	echo "maxz is $maxz"

	#echo "coverting $i to block median and then interpolated surface..."
	#cat $i | gmt blockmedian -C -I$cellsize -R${minx}/${maxx}/${miny}/${maxy} | gmt surface -I$cellsize -R${minx}/${maxx}/${miny}/${maxy} -G$(basename $i).nc -T0.35 -Ll-1.3758 -Lu0.0673 -V
	
	echo "creating surface"
	gmt surface $input_xyz -I$cellsize -R${minx}/${maxx}/${miny}/${maxy} -Gconv_grd.tif=gd:GTiff -T0.35 -Ll$minz -Lu$maxz -V
	
	#surface $i -R${minx}/${maxx}/${miny}/${maxy}  -G$(basename $i .xyz).nc -I$cellsize
	#echo "coverting $i interpolated surface to xyz..."
	#grd2xyz $(basename $i .xyz).nc | tr "\\t" "," > $(basename $i .xyz).nc.xyz
	#grdreformat $(basename $i .xyz).nc $(basename $i .xyz).nf -N -V
	#rm minmax_tmp.txt

else
	help

fi































