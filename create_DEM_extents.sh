#!/bin/sh -e
tile_extents=name_cell_extents_all.csv

# Get Tile Name, Cellsize, and Extents from tile_extents_gridding.txt
IFS=,
sed -n '/^ *[^#]/p' $tile_extents |
while read -r line
do
basename_=$(echo $line | awk '{print $1}')

echo "Processing" $basename_
gdal_calc.py -A $basename_"_DEM_smooth_10.tif"  --outfile=$basename_"_DEM_smooth_10_0.tif"  --calc="A*0"
gdal_polygonize.py $basename_"_DEM_smooth_10_0.tif" -f "ESRI Shapefile" $basename_"_DEM_final.shp"
rm $basename_"_DEM_smooth_10_0.tif"
#mv $basename_"_DEM_final.shp" e_fl_dems_review/$basename_"_DEM_final.shp"
echo "Created shp for" $basename_
echo

done
