dir_name=5186
shp_name=5186_clip_index_url_v2.shp
first_class=2
second_class=29

echo "Converting SHP to CSV"
ogr2ogr -f CSV $dir_name"_"clip_index_url.csv $shp_name

echo "Removing Header and Quotes"
sed '1d' $dir_name"_"clip_index_url.csv > tmpfile; mv tmpfile $dir_name"_"clip_index_url.csv
sed 's/"//' $dir_name"_"clip_index_url.csv > tmpfile; mv tmpfile $dir_name"_"clip_index_url.csv

mkdir -p xyz
mv $dir_name"_"clip_index_url.csv xyz/$dir_name"_"clip_index_url.csv
cd xyz

echo "Downloading Data"
wget -c -nc --input-file $dir_name"_"clip_index_url.csv

echo "Converting laz to xyz for class", $first_class
laz2xyz.sh $first_class

if [ -z "$second_class" ]
then
	echo "LAZ isn't topobathy and doesn't have second class"
	create_datalist.sh $dir_name"_lidar"
	#echo "$PWD/$dir_name"_lidar".datalist -1 1" >> $main_dir"/software/gridding/al_fl.datalist"
else
	echo "LAZ has valid second class"
	laz2xyz.sh $second_class
	echo "Separating Pos and Neg"
	separate_pos_neg.sh
	cd pos
	create_datalist.sh $dir_name"_lidar_pos"
	#echo "$PWD/$dir_name"_lidar_pos".datalist -1 1" >> $main_dir"/software/gridding/al_fl.datalist"
	cd ..
	cd neg 
	create_datalist.sh $dir_name"_lidar_neg"
	#echo "$PWD/$dir_name"_lidar_neg".datalist -1 1" >> $main_dir"/data/bathy/bathy_surf/al_fl_bs.datalist"
	cd ..
fi

