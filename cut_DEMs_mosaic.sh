#!/bin/sh
function help () {
echo "cut_DEMs_mosaic.sh - A script that cuts out DEM tiles from arcpy mosaic and resamples to appropriate resolution"
	echo "Usage: $0 mosaic_raster name_cell_extents"
	echo "* mosaic_raster: <mosaic raster generated from arcpy mosaic>"
	echo "* name_cell_extents: <cvs with name, cell, extents>"
}

if [ ${#@} == 2 ]; 
then

input_file=$1
tile_extents=$2


mkdir -p review

# Get Tile Name, Cellsize, and Extents from tile_extents_gridding.txt
IFS=,
sed -n '/^ *[^#]/p' $tile_extents |
while read -r line
do
basename_=$(echo $line | awk '{print $1}')
cellsize_degrees=$(echo $line | awk '{print $2}')
west=$(echo $line | awk '{print $3}')
east=$(echo $line | awk '{print $4}')
south=$(echo $line | awk '{print $5}')
north=$(echo $line | awk '{print $6}')
six_cells=$(echo "$cellsize_degrees * 6" | bc -l)
west_six_cells=$(echo "$west - $six_cells" | bc -l)
north_six_cells=$(echo "$north + $six_cells" | bc -l)
east_six_cells=$(echo "$east + $six_cells" | bc -l)
south_six_cells=$(echo "$south - $six_cells" | bc -l)

north_degree=${north:0:2}
north_decimal=${north:3:2}

if [ -z "$north_decimal" ]
then
	north_decimal="00"
else
	:
fi

size=${#north_decimal}
#echo "Number of North decimals is" $size
if [ "$size" = 1 ]
then
	north_decimal="$north_decimal"0
else
	:
fi


west_degree=${west:1:2}
west_decimal=${west:4:2}

if [ -z "$west_decimal" ]
then
	west_decimal="00"
else
	:
fi

size=${#west_decimal}
#echo "Number of West decimals is" $size
if [ "$size" = 1 ]
then
	west_decimal="$west_decimal"0
else
	:
fi


echo
echo "Input Tile Name is" $basename_
#echo "Cellsize in degrees is" $cellsize_degrees

if [ "$cellsize_degrees" = 0.000030864198718 ]
then
	cell_name=19
else
	cell_name=13
fi

#echo "East is" $east
#echo "South is" $south
echo "North is" $north
echo "North Degree is" $north_degree
echo "North Decimal is" $north_decimal

echo "West is" $west
echo "West Degree is" $west_degree
echo "West Decimal is" $west_decimal


#echo "West 6 Cells is" $west_six_cells
#echo "East 6 Cells is" $east_six_cells
#echo "South 6 Cells is" $south_six_cells
#echo "North 6 Cells is" $north_six_cells


echo "cutting out DEM ncei"$cell_name"_n"$north_degree"X"$north_decimal"_w0"$west_degree"X"$west_decimal"_2018v1.tif" 
#cut to shp
gdalwarp -cutline $basename_"_DEM_final.shp" -crop_to_cutline -of GTiff -dstnodata -9999 -tr $cellsize_degrees $cellsize_degrees $input_file $basename_"_DEM_tmp.tif"

#compress, set no data, etc.
#old method
#gdal_translate -of GTiff -a_srs EPSG:4269 -a_nodata -9999 -co "COMPRESS=DEFLATE" -co "PREDICTOR=3" -co "TILED=YES" -tr $cellsize_degrees $cellsize_degrees -projwin $west_six_cells $north_six_cells $east_six_cells $south_six_cells $input_file "ncei"$cell_name"_n"$north_degree"X"$north_decimal"_w0"$west_degree"X"$west_decimal"_2018v1.tif" -stats
#new method
gdal_translate -of GTiff -a_srs EPSG:4269 -a_nodata -9999 -co "COMPRESS=DEFLATE" -co "PREDICTOR=3" -co "TILED=YES" $basename_"_DEM_tmp.tif" "review/ncei"$cell_name"_n"$north_degree"X"$north_decimal"_w0"$west_degree"X"$west_decimal"_2018v1.tif" -stats
rm $basename_"_DEM_tmp.tif"
echo

done

else
	help
fi

