#!/bin/sh

function help () {
echo "final_dem_format - A script that uses name_cell_extents csv to create shp of DEM extents, cuts out DEM from mosaiced dataset, renames DEM to nw corner description, adds metadata info into tif, and converts the tif to netcdf .nc format for thredds server."
	echo "Usage: $0 name_cell_extents mosaic_tif smooth_factor"
	echo "* name_cell_extents: <csv with name, cellsize, and dem extents that were used to create DEMs>"
	echo "* mosaic_tif: <mosaic tif of multiple tiles created using arcpy>"
	echo "* smooth_factor: <the smooth factor you used previously on DEM, needed for correct variable name>"
}

name_cell_extents=$1
mosaic_tif=$2
smooth_factor=$3

#see if 2 parameters were provided
#show help if not
if [ ${#@} == 3 ]; 
then

mkdir -p deliverables
mkdir -p deliverables/thredds

# Get Tile Name, Cellsize, and Extents from tile_extents_gridding.txt
IFS=,
sed -n '/^ *[^#]/p' $name_cell_extents |
while read -r line
do
basename_=$(echo $line | awk '{print $1}')
cellsize_degrees=$(echo $line | awk '{print $2}')
west=$(echo $line | awk '{print $3}')
east=$(echo $line | awk '{print $4}')
south=$(echo $line | awk '{print $5}')
north=$(echo $line | awk '{print $6}')
north_degree=${north:0:2}
north_decimal=${north:3:2}

date=$(date --iso-8601=seconds)
echo date is $date

echo "Processing" $basename_
echo "Creating Shapefile of Extents"
gdaltindex $basename_"_DEM" $basename_"_DEM_smooth_"$smooth_factor".tif"

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

#echo
#echo "Input Tile Name is" $basename_
#echo "Cellsize in degrees is" $cellsize_degrees

if [ "$cellsize_degrees" = 0.00003086420 ]
then
	cell_name=19
else
	cell_name=13
fi

#echo "North is" $north
#echo "North Degree is" $north_degree
#echo "North Decimal is" $north_decimal

#echo "West is" $west
#echo "West Degree is" $west_degree
#echo "West Decimal is" $west_decimal

echo "cutting out DEM ncei"$cell_name"_n"$north_degree"X"$north_decimal"_w0"$west_degree"X"$west_decimal"_2019v1.tif" 
gdalwarp -cutline $basename_"_DEM"/$basename_"_DEM.shp" -crop_to_cutline -of GTiff -dstnodata -9999 -tr $cellsize_degrees $cellsize_degrees $mosaic_tif "ncei"$cell_name"_n"$north_degree"X"$north_decimal"_w0"$west_degree"X"$west_decimal"_2019v1_tmp.tif"
rm -r $basename_"_DEM"

echo "Adding metadata"
gdal_translate "ncei"$cell_name"_n"$north_degree"X"$north_decimal"_w0"$west_degree"X"$west_decimal"_2019v1_tmp.tif" -a_srs EPSG:4269 -a_nodata -9999 -mo TIFFTAG_COPYRIGHT="DOC/NOAA/NESDIS/NCEI > National Centers for Environmental Information, NESDIS, NOAA, U.S. Department of Commerce" -mo TIFFTAG_IMAGEDESCRIPTION="Topography-Bathymetry; NAVD88" -mo TIFFTAG_DATETIME=$date -co TILED=YES -co COMPRESS=DEFLATE -co PREDICTOR=3 "deliverables/ncei"$cell_name"_n"$north_degree"X"$north_decimal"_w0"$west_degree"X"$west_decimal"_2019v1.tif" -stats
rm "ncei"$cell_name"_n"$north_degree"X"$north_decimal"_w0"$west_degree"X"$west_decimal"_2019v1_tmp.tif"

echo "Converting to NetCDF nc for thredds"
#below method causes half cell shift in global mapper but not in arcgis. but when convert to xyz, it appears in right place in global mapper
gmt grdconvert "deliverables/ncei"$cell_name"_n"$north_degree"X"$north_decimal"_w0"$west_degree"X"$west_decimal"_2019v1.tif" "deliverables/thredds/ncei"$cell_name"_n"$north_degree"X"$north_decimal"_w0"$west_degree"X"$west_decimal"_2019v1.nc" -fg -V

# echo "Converting to NetCDF nc for thredds using previous version"
# gdal_translate "deliverables/ncei"$cell_name"_n"$north_degree"X"$north_decimal"_w0"$west_degree"X"$west_decimal"_2019v1.tif" -of netCDF "deliverables/thredds/ncei"$cell_name"_n"$north_degree"X"$north_decimal"_w0"$west_degree"X"$west_decimal"_2019v1.nc"
# gmt grdedit -T "deliverables/thredds/ncei"$cell_name"_n"$north_degree"X"$north_decimal"_w0"$west_degree"X"$west_decimal"_2019v1.nc"

done


else
	help

fi
