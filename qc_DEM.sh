#!/bin/sh -e
function help () {
echo "qc_DEM- Script that identifies possibly bad input data in a ROI and produces shell script to delete all files in ROI"
	echo "Usage: $0 name_cell_extents_qc datalist_qc "
	echo "* name_cell_extents_qc: <csv file with tile name, description,spatial resolution in decimal degrees,ROI in W,E,S,N>"
	echo "* datalist_qc: <master datalist file that points to individual datasets datalists>"
}
#see if 2 parameters were provided
#show help if not
if [ ${#@} == 2 ]; 
then
name_cell_extents=$1
datalist=$2
cwd=$(pwd)

# Get Tile Name, Cellsize, and Extents from name_cell_extents.csv
IFS=,
sed -n '/^ *[^#]/p' $name_cell_extents |
while read -r line
do
name=$(echo $line | awk '{print $1}')
descrip=$(echo $line | awk '{print $2}')
cellsize_degrees=$(echo $line | awk '{print $3}')
west_quarter=$(echo $line | awk '{print $4}')
east_quarter=$(echo $line | awk '{print $5}')
south_quarter=$(echo $line | awk '{print $6}')
north_quarter=$(echo $line | awk '{print $7}')


full_name=$name"_"$descrip

#if mb1 file exists for tile, use that.
if [ -f $"save_mb1/"$name"_DEM.mb-1" ]; then
	echo "Mb1 file exists, using as datalist"
	cp "save_mb1/"$name"_DEM.mb-1" $name".datalist"
	datalist=$(echo $name".datalist")
else
	echo "MB1 file doesn't exist, using orig datalist"
	datalist=$2
fi

echo "Datalist is" $datalist
echo

echo
echo "Tile Name is" $name
echo "Description is" $descrip
echo "Full name is" $full_name
echo "Cellsize in degrees is" $cellsize_degrees
echo "West is" $west_quarter
echo "East is" $east_quarter
echo "South is" $south_quarter
echo "North is" $north_quarter
echo "Datalist is" $datalist


#############################################################################
#############################################################################
#############################################################################
######################      DEM QC      #####################################
#############################################################################
#############################################################################
#############################################################################

#echo -- Creating interpolated DEM for tile $name
grid_dem=$full_name".grd"
#mb_range="-R$west_reduced/$east_reduced/$south_reduced/$north_reduced"
mb_range="-R$west_quarter/$east_quarter/$south_quarter/$north_quarter"
echo mb_range is $mb_range

# Run mbgrid
#echo --Running mbgrid...
# mbgrid -I$datalist -O$full_name \
# $mb_range \
# -A2 -D$x_dim_int/$y_dim_int -G3 -N \
# -C810000000/3 -S0 -F1 -T0.25 -X0.1

echo --Running mbgrid with no interpolation...
mbgrid -I$datalist -O$full_name $mb_range -E$cellsize_degrees"/"$cellsize_degrees"/degrees!" -A2 -G3 -N -C0 -S0 -F1

#echo -- Converting to tif
#gdal_translate $grid_dem -a_srs EPSG:4269 -a_nodata -99999 $full_name".tif"
gmt grdconvert $grid_dem $full_name".tif"=gd:GTiff
rm $grid_dem
rm $grid_dem".cmd"
rm $full_name".tif.aux.xml"

# create subdir and copy data used in gridding to subdir
mb1=$full_name".mb-1"
#make dir
new_dir=$name"/"$descrip
mkdir -p $new_dir

#mkdir -p "media/sf_external_hd/ga_sc_nc/data/qc/"$name
#mkdir -p "media/sf_external_hd/ga_sc_nc/data/qc/"$name"/"$descrip
mv $full_name".tif" $new_dir"/"$full_name".tif" 
mv $mb1 $new_dir"/"$mb1

cd $new_dir

mb1=$full_name".mb-1"
# Get Tile Name, Cellsize, and Extents from name_cell_extents.csv
IFS= 
sed -n '/^ *[^#]/p' $mb1 |
while read -r line
do
name_tmp=$(echo $line | awk '{print $1}')
name="${name_tmp:2}"
base=$(basename $name)
echo copying $base
dirname=$(dirname "$name_tmp") 
create_folder_tmp=$(echo $dirname | awk -Fdata '{print $NF}')
create_folder="${create_folder_tmp:1}"
mkdir -p $create_folder
cp $name $create_folder"/"$base
name_xyc="${name::-4}.xyc"
echo "mv $name $name_xyc" >> xyz2xyc.sh
done

cd ..
cd ..
IFS=,

done

else
	help
fi
