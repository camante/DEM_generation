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
os.chdir('..')

print "Unzipping NHD GDB"

print "Converting NHD GDB to Shapefile"

print "Merging NHD Shapefiles"

print "Clipping Merged NHD Shp to Study Area"

os.chdir('landsat')
print 'Clipping Landsat Shp to Study Area'
clip_landsat_cmd='ogr2ogr -clipsrc ' + study_area_shp + 'al_fl_landsat.shp ' + landsat_shp
os.system(clip_landsat_cmd)

print "Erasing NHD from Landsat"
erase_cmd='ogr2ogr al_fl_landsat_nhd.shp al_fl_nhd.shp -dialect SQLite -sql "SELECT ST_Difference(al_fl_nhd.geometry, al_fl_landsat.geometry) AS geometry FROM al_fl_nhd, 'al_fl_landsat.shp'.al_fl_landsat"'
#ogr2ogr difference.shp a.shp -dialect SQLite -sql "SELECT ST_Difference(a.geometry, b.geometry) AS geometry FROM a, 'b.shp'.b"
