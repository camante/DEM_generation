#!/bin/sh -e
function help () {
echo "download_lidar.sh Script to download lidar from NOAA's Digital Coast in a provided ROI shapefile"
	echo "Usage: $0 download_csv roi_shapefile "
	echo "* download_csv: <csv w urls of bulk_download tileindex.zip>"
	echo "* roi_shp: <master datalist file that points to individual datasets datalists>"
}

#see if 2 parameters were provided
#show help if not
if [ ${#@} == 2 ]; 
then
data_url=$1
roi_shp=$2

# Get URLs from csv
IFS=,
sed -n '/^ *[^#]/p' $1 |
while read -r line
do
data_url=$(echo $line | awk '{print $1}')
dir_name=$(echo $(basename $(dirname $data_url)))
mkdir -p $dir_name
cd $dir_name

echo "Downloading Index Shp"
wget $data_url

echo "Unzipping Index Shp"
unzip tileindex.zip

shp_name=$(ls *.shp)
echo "Index Shp name is " $shp_name

echo "Clipping Index Shp to ROI shp"
ogr2ogr -clipsrc $roi_shp $dir_name"_"clip_index.shp $shp_name

sql_var=$dir_name"_clip_index"
echo "Dropping all Columns but URL"
ogr2ogr -f "ESRI Shapefile" -sql "SELECT URL FROM '$sql_var'" $dir_name"_"clip_index_url.shp $dir_name"_"clip_index.shp

echo "Converting SHP to CSV"
ogr2ogr -f CSV $dir_name"_"clip_index_url.csv $dir_name"_"clip_index_url.shp

echo "Removing Header and Quotes"
sed '1d' $dir_name"_"clip_index_url.csv > tmpfile; mv tmpfile $dir_name"_"clip_index_url.csv
sed 's/"//' $dir_name"_"clip_index_url.csv > tmpfile; mv tmpfile $dir_name"_"clip_index_url.csv

mkdir -p laz
mv $dir_name"_"clip_index_url.csv laz/$dir_name"_"clip_index_url.csv
cd laz

echo "Downloading Data"
wget -c -nc --input-file $dir_name"_"clip_index_url.csv

cd ..
cd ..

done

else
	help
fi
