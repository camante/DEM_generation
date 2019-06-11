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

if not os.path.exists('shp'):
	os.makedirs('shp')

main_dir=sys.argv[1]
study_area_shp=sys.argv[2]
landsat_shp='/media/sf_win_lx/coastal_act/data/coast/landsat_all_NA.shp'

#tnmfetch.py -R /media/sf_external_hd/al_fl/data/study_area/al_fl_tiles_buff.shp -d 4:0 -f "FileGDB"
os.chdir('nhd')
print 'Downloading nhd from USGS'
nhd_download_cmd='tnmfetch.py -R ' + study_area_shp + ' -d 4:0 -f "FileGDB"' 
os.system(nhd_download_cmd)

print 'Moving all zip folders to main nhd dir'
move_zip_cmd="find . -name '*.zip*' -exec mv {} zip/ \; 2>/dev/null"
os.system(move_zip_cmd)

print "Unzipping NHD GDB"
os.chdir('zip')
unzip_cmd='unzip "*.zip"'
os.system(unzip_cmd)
os.chdir('..')
os.chdir('gdb')

print "Moving all gdb files to gdb dir"
move_gdb_cmd="find . -name '*.gdb' -exec mv {} gdb/ \; 2>/dev/null"
os.system(move_gdb_cmd)
os.chdir('gdb')

print "Converting NHD GDB to Shapefile"
for i in glob.glob("*gdb"):
	print "Processing File", i
	gdb_basename = i[:-4]
	create_nhd_shp_cmd = 'ogr2ogr -f "ESRI Shapefile" {} {} NHDArea -overwrite'.format(gdb_basename, i)
	subprocess.check_call(create_nhd_shp_cmd, shell=True)

print 'Moving all shp files to '
os.chdir('..')
move_shp_cmd="find . -name '*.shp*' -exec mv {} shp/ \; 2>/dev/null"
os.system(move_shp_cmd)
move_dbf_cmd="find . -name '*.dbf*' -exec mv {} shp/ \; 2>/dev/null"
os.system(move_dbf_cmd)
move_shx_cmd="find . -name '*.shx*' -exec mv {} shp/ \; 2>/dev/null"
os.system(move_shx_cmd)
move_prj_cmd="find . -name '*.prj*' -exec mv {} shp/ \; 2>/dev/null"
os.system(move_prj_cmd)

print "Merging NHD Shapefiles"
os.chdir('shp')
merge_shp='ogrmerge.py -single -o merge/nhdArea_merge.shp *.shp'
os.system(merge_shp)

print "Clipping Merged NHD Shp to Study Area"
os.chdir('merge')
clip_nhd_cmd='ogr2ogr -clipsrc ' + study_area_shp + 'al_fl_nhd.shp ' + 'ndhArea_merge.shp'
os.system(clip_nhd_cmd)
os.chdir('../../../..')

os.chdir('landsat')
print 'Clipping Landsat Shp to Study Area'
clip_landsat_cmd='ogr2ogr -clipsrc ' + study_area_shp + 'al_fl_landsat.shp ' + landsat_shp
os.system(clip_landsat_cmd)

print "Erasing NHD from Landsat"
erase_cmd='ogr2ogr al_fl_landsat_nhd.shp al_fl_nhd.shp -dialect SQLite -sql "SELECT ST_Difference(al_fl_nhd.geometry, al_fl_landsat.geometry) AS geometry FROM al_fl_nhd, 'al_fl_landsat.shp'.al_fl_landsat"'
os.system(erase_cmd)
