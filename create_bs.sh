#!/bin/sh -e
function help () {
echo "create_bs- Script that creates a bathy surface at 1 arc-sec for multiple DEM tiles, resamples it back to the target resolution, and converts it xyz. All inputs must be in same, local directory."
	echo "Usage: $0 name_cell_extents datalist coastline bs_res "
	echo "* name_cell_extents: <csv file with name,target spatial resolution in decimal degrees,tile_exents in W,E,S,N>"
	echo "* datalist: <master datalist file that points to individual datasets datalists>"
	echo "* coastline: <coastline shapefile for clipping. Don't include .shp extension >"
}

#see if 3 parameters were provided
#show help if not
if [ ${#@} == 3 ]; 
	then
	mkdir -p xyz
	mkdir -p topo_guide
	mkdir -p cmd
	mkdir -p save_mb1
	mkdir -p save_datalists
	mkdir -p tifs
	mkdir -p coast_shp
	mkdir -p nan_grds

	name_cell_extents=$1
	datalist_orig=$2
	coastline_full=$3

	#############################################################################
	#############################################################################
	#############################################################################
	######################      DERIVED VARIABLES     ###########################
	#############################################################################
	#############################################################################
	#############################################################################

	# Get Tile Name, Cellsize, and Extents from name_cell_extents.csv
	IFS=,
	sed -n '/^ *[^#]/p' $name_cell_extents |
	while read -r line
	do
	name=$(echo $line | awk '{print $1}')
	target_res=$(echo $line | awk '{print $2}')
	west_quarter=$(echo $line | awk '{print $3}')
	east_quarter=$(echo $line | awk '{print $4}')
	south_quarter=$(echo $line | awk '{print $5}')
	north_quarter=$(echo $line | awk '{print $6}')

	#if mb1 file already exists for tile, use that. This speeds up processing time if input data files didn't change.
	if [ -f $"save_mb1/"$name".mb-1" ]; then
		echo "Mb1 file exists, using as datalist"
		cp "save_mb1/"$name".mb-1" $name".datalist"
		datalist=$(echo $name".datalist")
	else
		echo "MB1 file doesn't exist, using orig datalist"
		cp $datalist_orig $name".datalist"
	fi

	datalist=$(echo $name".datalist")

	echo
	echo
	echo "Tile Name is" $name
	echo "Cellsize in degrees is" $target_res
	echo "West is" $west_quarter
	echo "East is" $east_quarter
	echo "South is" $south_quarter
	echo "North is" $north_quarter
	echo

	#Expand DEM extents by 6 cells to provide overlap between tiles
	six_cells_target=$(echo "$target_res * 6" | bc -l)
	#echo six_cells_target is $six_cells_target
	west=$(echo "$west_quarter - $six_cells_target" | bc -l)
	north=$(echo "$north_quarter + $six_cells_target" | bc -l)
	east=$(echo "$east_quarter + $six_cells_target" | bc -l)
	south=$(echo "$south_quarter - $six_cells_target " | bc -l)

	#Take in a half-cell on all sides so that grid-registered raster edge aligns exactly on desired extent
	half_cell=$(echo "$target_res / 2" | bc -l)
	echo half_cell is $half_cell
	west_reduced=$(echo "$west + $half_cell" | bc -l)
	north_reduced=$(echo "$north - $half_cell" | bc -l)
	east_reduced=$(echo "$east - $half_cell" | bc -l)
	south_reduced=$(echo "$south + $half_cell" | bc -l)

	mb_range="-R$west_reduced/$east_reduced/$south_reduced/$north_reduced"

	echo "West_reduced is" $west_reduced
	echo "East_reduced is" $east_reduced
	echo "South_reduced is" $south_reduced
	echo "North_reduced is" $north_reduced

	#Determine number of rows and columns with the desired cell size, rounding up to nearest integer.
	#i.e., 1_9 arc-second
	x_diff=$(echo "$east - $west" | bc -l)
	y_diff=$(echo "$north - $south" | bc -l)
	x_dim=$(echo "$x_diff / $target_res" | bc -l)
	y_dim=$(echo "$y_diff / $target_res" | bc -l)
	x_dim_int=$(echo "($x_dim+0.5)/1" | bc)
	y_dim_int=$(echo "($y_dim+0.5)/1" | bc)

	#############################################################################
	#############################################################################
	#############################################################################
	######################      Topo Guide     		  ###########################
	#############################################################################
	#############################################################################
	#############################################################################

	#Create Topo Guide for 1/9th Arc-Sec Topobathy DEMs

	if [ "$target_res" = 0.00003086420 ]
		then 
		echo -- Creating Topo Guide... 
		#This adds in values of zero to constain interpolation in inland areas without data.
		dem_name_tg=$name"_topo_guide"
		grid_dem_tg=$dem_name_tg".grd"
		#create empty datalist
		touch dummy.datalist
		#echo mb_range is $mb_range
		# Run mbgrid
		#echo --Running mbgrid...
		mbgrid -Idummy.datalist -O$dem_name_tg \
		$mb_range \
		-A2 -D$x_dim_int/$y_dim_int -G3 -N \
		-C0/0 -S0 -F1 -T0.25

		# Get Grid Area
		echo -- Reclasifying any NaNs to 0s

		#export GDAL_NETCDF_BOTTOMUP=NO
		#gmt set IO_NC4_CHUNK_SIZE 2
		gmt grdconvert $grid_dem_tg $grid_dem_tg".tif"=gd:GTiff

		gdal_calc.py -A $grid_dem_tg".tif" --outfile=$grid_dem_tg"_fix_nan.tif" --calc="nan_to_num(A)" --overwrite
		rm $grid_dem_tg".tif"

		echo -- Getting the extents of the raster
		x_min_tmp=`gmt grdinfo $grid_dem_tg | grep -e "x_min" | awk '{print $3}'`
		x_max_tmp=`gmt grdinfo $grid_dem_tg | grep -e "x_max" | awk '{print $5}'`
		y_min_tmp=`gmt grdinfo $grid_dem_tg | grep -e "y_min" | awk '{print $3}'`
		y_max_tmp=`gmt grdinfo $grid_dem_tg | grep -e "y_max" | awk '{print $5}'`

		#Add on 6 more cells just to make sure there is no edge effects when burnining in shp.
		x_min=$(echo "$x_min_tmp - $six_cells_target" | bc -l)
		x_max=$(echo "$x_max_tmp + $six_cells_target" | bc -l)
		y_min=$(echo "$y_min_tmp - $six_cells_target" | bc -l)
		y_max=$(echo "$y_max_tmp + $six_cells_target" | bc -l)

		#echo $x_min $y_min $x_max $y_max

		echo -- Clipping coastline shp to grid extents
		ogr2ogr $name"_coast.shp" $coastline_full".shp" -clipsrc $x_min $y_min $x_max $y_max

		echo -- Setting Topo to -0.1 Prior to Gridding
		gdal_rasterize -burn -0.1 -l $name"_coast" $name"_coast.shp" $grid_dem_tg"_fix_nan.tif"


		#Tiling
		tile_x_div=12
		tile_y_div=12

		#get input grid dimensions
		x_dim=`gdalinfo $grid_dem_tg"_fix_nan.tif" | grep -e "Size is" | awk '{print $3}' | sed 's/.$//'`
		y_dim=`gdalinfo $grid_dem_tg"_fix_nan.tif" | grep -e "Size is" | awk '{print $4}'`

		#calculate tile grid dimensions
		tile_dim_x_tmp=$(echo "$x_dim / $tile_x_div" | bc -l)
		tile_dim_x_int=$(echo "($tile_dim_x_tmp+0.5)/1" | bc)

		tile_dim_y_tmp=$(echo "$y_dim / $tile_y_div" | bc -l)
		tile_dim_y_int=$(echo "($tile_dim_y_tmp+0.5)/1" | bc)

		#initiate tile names with numbers, starting with 1
		tile_name="1"
		#remove file extension to get basename from input file
		input_name=${input_file::-4}
		#starting point for tiling
		xoff=0
		yoff=0

		while [ "$(bc <<< "$xoff < $x_dim")" == "1"  ]; do
		    yoff=0
		    while [ "$(bc <<< "$yoff < $y_dim")" == "1"  ]; do
		    tile_name_full="guide_xyz_"$name"_t"$tile_name".tif"
		    echo creating tile $tile_name_full
		    echo xoff is $xoff
		    echo yoff is $yoff
		    echo tile_dim_x_int is $tile_dim_x_int
		    echo tile_dim_y_int $tile_dim_y_int
		    gdal_translate -of GTiff -a_nodata 999999 -srcwin $xoff $yoff $tile_dim_x_int $tile_dim_y_int $grid_dem_tg"_fix_nan.tif" $tile_name_full -stats
		    z_min=`gmt grdinfo $tile_name_full | grep -e "z_min" | awk '{print $3}'`
		    echo "z_min is" $z_min
		    if (( $(echo "$z_min > -0.000001" | bc -l) ));
			then
			      echo "tile is all bathy data with zeroes, deleting..."
			      rm $tile_name_full
			else
			      echo "tile has data, keeping..."
			      echo -- Converting to xyz, only keeping negative values
			      gdal_translate -of XYZ $tile_name_full $tile_name_full"_tmp.xyz"
			      awk '{if ($3 < -0.00) {printf "%.7f %.7f %.2f\n", $1,$2,$3}}' $tile_name_full"_tmp.xyz" > $tile_name_full".xyz"
			      echo -- Converted to xyz
			      rm $tile_name_full
			      rm $tile_name_full"_tmp.xyz"
			      mv $tile_name_full".xyz" topo_guide/$tile_name_full".xyz" 
			fi
			yoff=$(echo "$yoff+$tile_dim_y_int" | bc)
		    tile_name=$((tile_name+1))
		    done
		  xoff=$(echo "$xoff+$tile_dim_x_int" | bc)
		done
		
		rm $grid_dem_tg"_fix_nan.tif"
		
		echo -- Creating Datalist for Topo Guide
		cd topo_guide

		#cat 
		cat *guide_xyz* >  $name"_topo_guide_all.xyz"
		rm *guide_xyz*

		echo -- Randomly Sample 10000 xyz pnts
		shuf -n 10000 $name"_topo_guide_all.xyz" > $name"_tguide.xyz"

		rm $name"_topo_guide_all.xyz"

		ls *.xyz > temp
		awk '{print $1, 168}' temp > topo_guide.datalist
		rm temp
		mbdatalist -F-1 -Itopo_guide.datalist -O -V
		#
		echo
		echo "All done"
		cd .. 
		rm $grid_dem_tg
		rm $dem_name_tg".mb-1"
		rm $grid_dem_tg".tif.aux.xml"

	else
		echo "DEM is bathy 1/3rd, no need for topo guide"
	fi


	#############################################################################
	#############################################################################
	#############################################################################
	######################      BATHY SURFACE    		  #######################
	#############################################################################
	#############################################################################
	#############################################################################
	#echo -- Creating interpolated DEM for tile $name
	dem_name=$name
	grid_dem=$dem_name".grd"
	echo mb_range is $mb_range
	# Run mbgrid
	echo --Running mbgrid...
	mbgrid -I$datalist -O$dem_name \
	$mb_range \
	-A2 -D$x_dim_int/$y_dim_int -G3 -N \
	-C810000000/3 -S0 -F1 -T0.25 -X0.1

	#Check to see if any valid data
	z_min=`gmt grdinfo $grid_dem | grep -e "z_min" | awk '{print $3}'`
	z_max=`gmt grdinfo $grid_dem | grep -e "z_max" | awk '{print $5}'`
	echo "z_min is" $z_min
	echo "z_max is" $z_max

	#If 1/3rd, I need to create shp.
	if [ "$target_res" != 0.00003086420 ]
	then
		echo -- Getting the extents of the raster
		x_min_tmp=`gmt grdinfo $grid_dem | grep -e "x_min" | awk '{print $3}'`
		x_max_tmp=`gmt grdinfo $grid_dem | grep -e "x_max" | awk '{print $5}'`
		y_min_tmp=`gmt grdinfo $grid_dem | grep -e "y_min" | awk '{print $3}'`
		y_max_tmp=`gmt grdinfo $grid_dem | grep -e "y_max" | awk '{print $5}'`

		#Add on 6 more cells just to make sure there is no edge effects when burnining in shp.
		x_min=$(echo "$x_min_tmp - $six_cells_target" | bc -l)
		x_max=$(echo "$x_max_tmp + $six_cells_target" | bc -l)
		y_min=$(echo "$y_min_tmp - $six_cells_target" | bc -l)
		y_max=$(echo "$y_max_tmp + $six_cells_target" | bc -l)

		#echo $x_min $y_min $x_max $y_max
		echo -- Clipping coastline shp to grid extents
		ogr2ogr $name"_coast.shp" $coastline_full".shp" -clipsrc $x_min $y_min $x_max $y_max

	else
		echo -- Already created shp for 1/9th arc-sec DEM topo guide
	fi


	gmt grdconvert $grid_dem $grid_dem".tif"=gd:GTiff

	if [ "$z_min" = "NaN" ] && [ "$z_max" = "NaN" ]
	then
	      	echo "Tile has no data, moving to nan_grds folder..."
	      	echo -- Reclasifying any NaNs to 0s
			gdal_calc.py -A $grid_dem".tif" --outfile=$grid_dem"_zeroes.tif" --calc="nan_to_num(A)" --overwrite
	      	rm $grid_dem".tif"
	      	mv $grid_dem"_zeroes.tif" nan_grds/$grid_dem"_zeroes.tif"
	      	rm $name".mb-1"
			rm $name"_coast.shp" 
			rm $name"_coast.dbf" 
			rm $name"_coast.prj" 
			rm $name"_coast.shx"
			rm $datalist
	else
	      	echo "tile has data, keeping..."

	      	echo -- Reclasifying any NaNs to 0s
	      	gdal_calc.py -A $grid_dem".tif" --outfile=$grid_dem"_fix_nan.tif" --calc="nan_to_num(A)" --overwrite
	      	
	      	echo -- Changing any 0 or above to -0.1m
			gdal_calc.py -A $grid_dem"_fix_nan.tif" --outfile=$grid_dem"_rc.tif" --calc="-0.1*(A >= 0.0)+A*(A < 0.0)" --format=GTiff --overwrite
			rm $grid_dem".tif"
			rm $grid_dem"_fix_nan.tif"

			echo -- Masking out Topo
			gdal_rasterize -burn 1 -l $name"_coast" $name"_coast.shp" $grid_dem"_rc.tif"

			echo -- Compressing tif
			gdal_translate $grid_dem"_rc.tif" -a_srs EPSG:4269 -a_nodata 999999 -co "COMPRESS=DEFLATE" -co "PREDICTOR=3" -co "TILED=YES" $name"_target_res.tif"
			rm $grid_dem"_rc.tif"

			#If bathy mask file exists, mask out additional topo
			if [ -f $name"_DEM_bathy_1_0.tif" ]; then
				echo "Bathy Mask exists, masking out additional topo areas"
				echo -- Masking out additional topo from DEM
				gdal_calc.py -A $name"_target_res.tif" -B $name"_DEM_bathy_1_0.tif" --outfile=$name"_target_res_final_tmp.tif" --calc="A*B"
				gdal_translate $name"_target_res_final_tmp.tif" -a_srs EPSG:4269 -a_nodata -99999 -co "COMPRESS=DEFLATE" -co "PREDICTOR=3" -co "TILED=YES" $name"_bs.tif"
				rm $name"_target_res_final_tmp.tif"
			else
				echo "Bathy Mask doesn't exist, skipping..."
				mv $name"_target_res.tif" $name"_bs.tif"
			fi

			echo -- Tiling Bathy Surface and Converting to XYZ
			#Input parameters
			input_file=${name}"_bs.tif"

			cp $input_file tifs/$input_file
			mv $name".mb-1" save_mb1/$name".mb-1"
			mv $name"_coast.shp" coast_shp/$name"_coast.shp"
			mv $name"_coast.dbf" coast_shp/$name"_coast.dbf"
			mv $name"_coast.prj" coast_shp/$name"_coast.prj"
			mv $name"_coast.shx" coast_shp/$name"_coast.shx"
			mv $datalist save_datalists/$datalist



			#Convert tif to xyz for 1/9th arc-sec

			if [ "$target_res" = 0.00003086420 ]
			then 
				#8112 and 2712 are both divisible by 8, create 64 tiles
				#or by 12, create 144 tiles
				tile_x_div=12
				tile_y_div=12

				###################################################################################
				###################################################################################
				#tile_x_pct_tmp=$(echo "100 / $tile_x_pct" | bc -l)
				#tile_y_pct_tmp=$(echo "100 / $tile_y_pct" | bc -l)

				#get input grid dimensions
				x_dim=`gdalinfo $input_file | grep -e "Size is" | awk '{print $3}' | sed 's/.$//'`
				y_dim=`gdalinfo $input_file | grep -e "Size is" | awk '{print $4}'`

				#calculate tile grid dimensions
				tile_dim_x_tmp=$(echo "$x_dim / $tile_x_div" | bc -l)
				tile_dim_x_int=$(echo "($tile_dim_x_tmp+0.5)/1" | bc)

				tile_dim_y_tmp=$(echo "$y_dim / $tile_y_div" | bc -l)
				tile_dim_y_int=$(echo "($tile_dim_y_tmp+0.5)/1" | bc)

				#OR, you can just manually input the number of rows/cols you want
				#tile_dim_x_int=ENTER NUMBER OF COLUMNS HERE
				#tile_dim_y_int=ENTER NUMBER OF ROWS HERE
				#Example; to create 100 tiles when original dimensions are 475100, 61450:
				
				#tile_dim_x_int=1014
				#tile_dim_y_int=1014

				echo input grid is $input_file	

				echo input grid x_dim is $x_dim
				echo input grid y_dim is $y_dim

				echo tile x_dim is $tile_dim_x_int
				echo tile y_dim is $tile_dim_y_int

				echo
				echo -- Starting Tile Analysis on 1/9th arc-sec DEMs
				echo

				#initiate tile names with numbers, starting with 1
				tile_name="1"
				#remove file extension to get basename from input file
				input_name=${input_file::-4}
				#starting point for tiling
				xoff=0
				yoff=0

				while [ "$(bc <<< "$xoff < $x_dim")" == "1"  ]; do
				    yoff=0
				    while [ "$(bc <<< "$yoff < $y_dim")" == "1"  ]; do
				    tile_name_full=$input_name"_tile_"$tile_name".tif"
				    echo creating tile $tile_name_full
				    echo xoff is $xoff
				    echo yoff is $yoff
				    echo tile_dim_x_int is $tile_dim_x_int
				    echo tile_dim_y_int $tile_dim_y_int
				    gdal_translate -of GTiff -a_nodata 999999 -srcwin $xoff $yoff $tile_dim_x_int $tile_dim_y_int $input_file $tile_name_full -stats
				    z_min=`gmt grdinfo $tile_name_full | grep -e "z_min" | awk '{print $3}'`
				    #valid_check=
				    #check to see if tile has data, and detele if no valid values.
				    #valid_check=`gdalinfo $tile_name_full | grep -e "STATISTICS_MAXIMUM"`
				    echo "z_min is" $z_min
				    if (( $(echo "$z_min > 0" | bc -l) ));
					then
					      echo "tile has no data, deleting..."
					      rm $tile_name_full
					else
					      echo "tile has data, keeping..."
					      echo -- Converting to xyz, only keeping negative values
					      gdal_translate -of XYZ $tile_name_full $tile_name_full"_tmp.xyz"
					      awk '{if ($3 < -0.00) {printf "%.7f %.7f %.2f\n", $1,$2,$3}}' $tile_name_full"_tmp.xyz" > $tile_name_full".xyz"
					      echo -- Converted to xyz
					      rm $tile_name_full
					      rm $tile_name_full"_tmp.xyz" 
					      mv $tile_name_full".xyz" xyz/$tile_name_full".xyz"
					fi
					yoff=$(echo "$yoff+$tile_dim_y_int" | bc)
				    tile_name=$((tile_name+1))
				    done
				  xoff=$(echo "$xoff+$tile_dim_x_int" | bc)
				done
				echo -- Creating Datalist for Bathy Surface XYZ
				cd xyz/
				ls *.xyz > temp
				awk '{print $1, 168}' temp > bathy_surf.datalist
				rm temp
				mbdatalist -F-1 -Ibathy_surf.datalist -O -V
				#
				echo
				echo "All done"
				cd ..
			
			else
				echo "Tif is 1/3rd, not converting to xyz"
			fi
	fi

	rm $grid_dem".tif.aux.xml"
	rm $grid_dem
	rm $name"_bs.tif"

	if [ -f $name".grd.cmd" ]; then
		echo "cmd file exists, move to subdir"
		mv $name".grd.cmd" cmd/$name".grd.cmd"
	else
		echo "cmd file didn't exist"
	fi

	done

else
	help
fi
