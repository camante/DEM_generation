'''
Description:
-Download USGS NHDPlus with fetch
-unzip
-convert gdb to shp Hydrography/NHDArea
-merge shp
-clip landsat derived to study area
-erase nhd areas from landsat derived data

Author:
Chris Amante
Christopher.Amante@colorado.edu

Date:
6/5/2019

'''
#################################################################
#################################################################
#################################################################
####################### IMPORT MODULES ##########################
#################################################################
#################################################################
#################################################################
import os
import sys
import glob
######################## NOS ####################################
print "Current directory is ", os.getcwd()

if not os.path.exists('nhd'):
	os.makedirs('nhd')

if not os.path.exists('nhd/zip'):
	os.makedirs('nhd/zip')

if not os.path.exists('nhd/gdb'):
	os.makedirs('nhd/gdb')

if not os.path.exists('nhd/shp'):
	os.makedirs('nhd/shp')

if not os.path.exists('nhd/shp/merge'):
	os.makedirs('nhd/shp/merge')

if not os.path.exists('landsat'):
	os.makedirs('landsat')

#Params from master script:
#main_dir=sys.argv[1]
#study_area_shp=sys.argv[2]
#roi_str_ogr=sys.argv[3]+' '+sys.argv[4]+' '+sys.argv[5]+' '+sys.argv[6]
#Hard-coded to test
main_dir='/media/sf_external_hd/al_fl'
study_area_shp=main_dir + '/data/study_area/al_fl_tiles_buff.shp'
roi_str_ogr='-88.525 29.225 -83.975 31.525'
roi_str_gmt='-88.525/-83.975/29.225/31.525'

#Additional Params:
landsat_shp='/media/sf_win_lx/coastal_act/data/coast/landsat_all_NA.shp'
#script removes disconnected rivers by only keep the largest poly (num_nhd_polys=1). 
#If need large disconnected rivers,esp. on tile edges that got cut off, make value higher, e.g. num_nhd_polys=2.
num_nhd_polys='7'




############ ANALYSIS ##################



# print "Rasterizing Study Area w Buff"
# rast_study_area_cmd = 'gdal_rasterize -tr 0.00003086420 0.00003086420 -te ' + roi_str_ogr + ' -burn 0 -ot Int16 -co COMPRESS=DEFLATE ' + study_area_shp + ' al_fl_tiles_buff.tif'
# os.system(rast_study_area_cmd)

# print "Copying Raster to burn clean NHD"
# cp_cmd = 'cp al_fl_tiles_buff.tif nhd/al_fl_nhd_clean.tif'
# os.system(cp_cmd)

# print "Copying Raster to burn Landsat"
# cp_cmd2 = 'cp al_fl_tiles_buff.tif landsat/al_fl_landsat.tif'
# os.system(cp_cmd2)

os.chdir('nhd')
# print 'Downloading nhd from USGS'
# nhd_download_cmd='tnmfetch.py -R ' + roi_str_gmt + ' -d 4:0 -f "FileGDB"' 
# os.system(nhd_download_cmd)

# print 'Moving all zip folders to main nhd dir'
# move_zip_cmd="find . -name '*.zip*' -exec mv {} zip/ \; 2>/dev/null"
# os.system(move_zip_cmd)

# print "Unzipping NHD GDB"
# os.chdir('zip')
# unzip_cmd='unzip "*.zip"'
# os.system(unzip_cmd)
# os.chdir('..')

# print "Moving all gdb files to gdb dir"
# move_gdb_cmd="find . -name '*.gdb' -exec mv {} gdb/ \; 2>/dev/null"
# os.system(move_gdb_cmd)
# os.chdir('gdb')

# print "Converting NHD GDB to Shapefile"
# for i in glob.glob("*gdb"):
# 	print "Processing File", i
# 	gdb_basename = i[:-4]
# 	create_nhd_shp_cmd = 'ogr2ogr -f "ESRI Shapefile" {} {} NHDArea -overwrite'.format(gdb_basename, i)
# 	os.system(create_nhd_shp_cmd)
# 	#rename files
# 	rename_shp_cmd = 'mv {}/NHDArea.shp {}/{}_NHDArea.shp'.format(gdb_basename, gdb_basename, gdb_basename)
# 	os.system(rename_shp_cmd)
# 	rename_dbf_cmd = 'mv {}/NHDArea.dbf {}/{}_NHDArea.dbf'.format(gdb_basename, gdb_basename, gdb_basename)
# 	os.system(rename_dbf_cmd)
# 	rename_shx_cmd = 'mv {}/NHDArea.shx {}/{}_NHDArea.shx'.format(gdb_basename, gdb_basename, gdb_basename)
# 	os.system(rename_shx_cmd)
# 	rename_prj_cmd = 'mv {}/NHDArea.prj {}/{}_NHDArea.prj'.format(gdb_basename, gdb_basename, gdb_basename)
# 	os.system(rename_prj_cmd)

# 	create_nhd_shp_cmd2 = 'ogr2ogr -f "ESRI Shapefile" {} {} NHDPlusBurnWaterbody -overwrite'.format(gdb_basename, i)
# 	os.system(create_nhd_shp_cmd2)
# 	#rename files
# 	rename_shp_cmd = 'mv {}/NHDPlusBurnWaterbody.shp {}/{}_NHDPlusBurnWaterbody.shp'.format(gdb_basename, gdb_basename, gdb_basename)
# 	os.system(rename_shp_cmd)
# 	rename_dbf_cmd = 'mv {}/NHDPlusBurnWaterbody.dbf {}/{}_NHDPlusBurnWaterbody.dbf'.format(gdb_basename, gdb_basename, gdb_basename)
# 	os.system(rename_dbf_cmd)
# 	rename_shx_cmd = 'mv {}/NHDPlusBurnWaterbody.shx {}/{}_NHDPlusBurnWaterbody.shx'.format(gdb_basename, gdb_basename, gdb_basename)
# 	os.system(rename_shx_cmd)
# 	rename_prj_cmd = 'mv {}/NHDPlusBurnWaterbody.prj {}/{}_NHDPlusBurnWaterbody.prj'.format(gdb_basename, gdb_basename, gdb_basename)
# 	os.system(rename_prj_cmd)


# print 'Moving all shp files to shp dir'
# os.chdir('..')
# move_shp_cmd="find . -name '*.shp*' -exec mv {} shp/ \; 2>/dev/null"
# os.system(move_shp_cmd)
# move_dbf_cmd="find . -name '*.dbf*' -exec mv {} shp/ \; 2>/dev/null"
# os.system(move_dbf_cmd)
# move_shx_cmd="find . -name '*.shx*' -exec mv {} shp/ \; 2>/dev/null"
# os.system(move_shx_cmd)
# move_prj_cmd="find . -name '*.prj*' -exec mv {} shp/ \; 2>/dev/null"
# os.system(move_prj_cmd)

# print "Merging NHD Shapefiles"
# os.chdir('shp')
# merge_shp_cmd='for f in *.shp; do ogr2ogr -update -append merge/nhdArea_merge.shp $f -f "ESRI Shapefile"; done;'
# os.system(merge_shp_cmd)


# os.chdir('..')
# print roi_str_ogr


# print "Clipping Merged NHD Shp to Study Area"
# clip_nhd_cmd='ogr2ogr -clipsrc ' + roi_str_ogr + ' al_fl_nhd.shp ' + 'shp/merge/nhdArea_merge.shp'
# #ogr2ogr -clipsrc -88.5 30.25 -88.25 30.5 al_fl_nhd_test.shp shp/merge/nhdArea_merge.shp
# os.system(clip_nhd_cmd)

# print "Rasterizing Shp"
# raster_shp_cmd = "gdal_rasterize -tr 0.00003086420 0.00003086420 -burn 1 -ot Int16 -co COMPRESS=DEFLATE al_fl_nhd.shp al_fl_nhd.tif"
# #gdal_rasterize -tr 0.00003086420 0.00003086420 -burn 1 -ot Int16 -co COMPRESS=DEFLATE al_fl_nhd_test.shp al_fl_nhd_test.tif
# os.system(raster_shp_cmd)

# print "Polygonizing Raster"
# poly_rast_cmd = "gdal_polygonize.py -8 -f 'ESRI Shapefile' al_fl_nhd.tif al_fl_nhd_rast.shp"
# #gdal_polygonize.py -8 -f 'ESRI Shapefile' al_fl_nhd_test.tif al_fl_nhd_rast_test.shp
# os.system(poly_rast_cmd)

# print "Removing Disconnected Rivers"
# rm_polys_cmd = '''ogr2ogr -dialect SQLITE -sql "SELECT * FROM al_fl_nhd_rast WHERE DN='1' order by ST_AREA(geometry) desc limit {}" al_fl_nhd_clean.shp al_fl_nhd_rast.shp'''.format(num_nhd_polys)
# #ogr2ogr -dialect SQLITE -sql "SELECT * FROM al_fl_nhd_rast_test WHERE DN='1' order by ST_AREA(geometry) desc limit 2" al_fl_nhd_clean_test.shp al_fl_nhd_rast_test.shp
# os.system(rm_polys_cmd)

print "Re-Rasterizing Shp"
raster_shp_cmd = "gdal_rasterize -burn 1 -l al_fl_nhd_clean al_fl_nhd_clean.shp al_fl_nhd_clean.tif"
#gdal_rasterize -tr 0.00003086420 0.00003086420 -burn 0 -ot Int16 -co COMPRESS=DEFLATE  -te -88.5 30.25 -88.25 30.5 al_fl_nhd_clean_test.tif
#gdal_rasterize -burn 1 -l al_fl_nhd_clean al_fl_nhd_clean_test.shp al_fl_nhd_clean_test.tif
os.system(raster_shp_cmd)

os.chdir('..')

os.chdir('landsat')
print 'Clipping Landsat Shp to Study Area'
clip_landsat_cmd='ogr2ogr -clipsrc ' + roi_str_ogr + ' al_fl_landsat.shp ' + landsat_shp
os.system(clip_landsat_cmd)

print "Rasterizing Landsat Shp"
raster_shp_cmd2 = "gdal_rasterize -i -burn 1 -l al_fl_landsat al_fl_landsat.shp al_fl_landsat.tif"
#gdal_rasterize -tr 0.00003086420 0.00003086420 -burn 0 -ot Int16 -co COMPRESS=DEFLATE  -te -88.5 30.25 -88.25 30.5 al_fl_landsat.shp al_fl_landsat_test.tif
os.system(raster_shp_cmd2)

os.chdir('..')

print "Adding NHD and Landsat Rasters"
add_rasts_cmd = 'gdal_calc.py -A nhd/al_fl_nhd_clean.tif -B landsat/al_fl_landsat.tif --outfile=al_fl_coast_sum.tif --calc="A + B" --format=GTiff --overwrite'
#gdal_calc.py -A nhd/al_fl_nhd_clean_test.tif -B landsat/al_fl_landsat_test.tif --outfile=al_fl_coast_sum_test.tif --calc="A + B" --format=GTiff --overwrite
os.system(add_rasts_cmd)

print "Reclassifying Rasters"
rc_rast_cmd2 = 'gdal_calc.py -A al_fl_coast_sum.tif --outfile=al_fl_coast_rc_tmp.tif --calc="1*(A > 0)" --format=GTiff --overwrite'
#gdal_calc.py -A al_fl_coast_sum_test.tif --outfile=al_fl_coast_rc_test.tif --calc="1*(A > 0)" --format=GTiff --overwrite
os.system(rc_rast_cmd2)

rm_rast_cmd = 'rm al_fl_coast_sum.tif'
os.system(rm_rast_cmd)

print "Compressing Tif"
compress_tif_cmd = 'gdal_translate al_fl_coast_rc_tmp.tif -co "COMPRESS=DEFLATE" -co "TILED=YES" al_fl_coast_rc.tif'
os.system(compress_tif_cmd)

rm_rast_cmd2 = 'rm al_fl_coast_rc_tmp.tif'
os.system(rm_rast_cmd2)

print "Polygonizing Re-classified Raster"
poly_rc_rast_cmd = "gdal_polygonize.py -8 -f 'ESRI Shapefile' al_fl_coast_rc.tif al_fl_coast_all.shp"
#gdal_polygonize.py -8 -f 'ESRI Shapefile' al_fl_coast_rc_test.tif al_fl_coast_all_test.shp
os.system(poly_rc_rast_cmd)

print "Removing Bathy Areas"
rm_bathy_cmd = '''ogr2ogr -dialect SQLITE -sql "SELECT * FROM al_fl_coast_all WHERE DN='0'" al_fl_coast.shp al_fl_coast_all.shp'''
#ogr2ogr -dialect SQLITE -sql "SELECT * FROM al_fl_coast_all_test WHERE DN='0'" al_fl_coast_test.shp al_fl_coast_all_test.shp
os.system(rm_bathy_cmd)
