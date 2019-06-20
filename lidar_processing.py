'''
Description:
-Download lidar by clipping digital coast index shp to study area poly
-Some datasets don't work with fetch. Need to download manually?
-Clip superceded datasets with Matt's ogr?
-Convert to xyz
-Separate topo and topo bathy.
-Separate topobathy into pos and neg. Neg goes into bathy surface.

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

if not os.path.exists('lidar'):
	os.makedirs('lidar')

main_dir=sys.argv[1]
study_area_shp=sys.argv[2]

#other params
dc_lidar_download=dc_lidar_download.csv

os.chdir('lidar')
print 'Downloading lidar from Digital Coast'

lidar_download_cmd='download_process_lidar.sh ' + main_dir + '/data/' + dc_lidar_download + ' ' + study_area_shp
os.system(lidar_download_cmd)

#Download any datasets with bad digital coast index.shp


