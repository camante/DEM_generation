'''
Description:
Master Script to Generate DEMs for AL and FL. 

Author:
Chris Amante
Christopher.Amante@colorado.edu

Date:
5/22/2019

'''
#################################################################
#################################################################
#################################################################
####################### IMPORT MODULES ##########################
#################################################################
#################################################################
#################################################################
import os
import subprocess
import sys
import glob
#################################################################
#################################################################
#################################################################
###################### INITIAL VARIABLES ########################
#################################################################
#################################################################
#################################################################
code_dir='/media/sf_external_hd/al_fl/code/DEM_generation'
main_dir='/media/sf_external_hd/al_fl'
name_cell_extents='/media/sf_external_hd/al_fl/data/study_area/name_cell_extents.csv'
#name_cell_extents='/media/sf_external_hd/al_fl/data/study_area/name_cell_extents_test.csv'

os.chdir(main_dir)
print 'Main Directory is', os.getcwd()
#Creating main subdirectories
dir_list=['data', 'docs', 'software', 'software/gridding']
for i in dir_list:
	if not os.path.exists(i):
		print 'creating subdir', i
		os.makedirs(i)

#ROI for data download
west_buff=-88.525
east_buff=-83.975
south_buff=29.225
north_buff=31.525
roi_str=str(west_buff)+'/'+str(east_buff)+'/'+str(south_buff)+'/'+str(north_buff)
#-88.525/-83.975/29.225/31.525
#test_ROI
#roi_str='-88.5/-88.49/29.99/30'
print "ROI is", roi_str
#################################################################
#################################################################
#################################################################
####################### PRE-PROCESSING ##########################
#################################################################
#################################################################
#################################################################
#Create Conversion Grid -- MLLW to NAVD88
if not os.path.exists('data/conv_grd'):
	os.makedirs('data/conv_grd')

os.chdir('data/conv_grd')
#print "Creating mllw2navd88 conversion grid"
#conv_grd_cmd='dem cgrid -i mllw -o navd88 -c -E 1s -R' +roi_str
#os.system(conv_grd_cmd)

conv_grd_path=main_dir+'/data/conv_grd/cgrid_mllw2navd88.tif'
#################################################################
#################################################################
#################################################################
####################### DATA DOWNLOAD ###########################
#################################################################
#################################################################
#################################################################
os.chdir('..')

#################################################################
####################### STUDY AREA ##############################
#################################################################
#manually created fishnet shp in Global Mapper (al_fl_tiles.shp) 
#created name_cell_extents with arcpy get_poly_coords.py (name_cell_extents.csv) 
#manually created study area buffer in ArcMap (al_fl_tiles_buff.shp)

#################################################################
######################## COASTLINE ##############################
#################################################################

#################################################################
########################## BATHY ################################
#################################################################
#Creating main subdirectories
os.chdir('bathy')

bathy_dir_list=['usace_dredge', 'mb', 'nos']
#bathy_dir_list=['/media/sf_external_hd/test/usace_dredge']
for i in bathy_dir_list:
	if not os.path.exists(i):
		print 'creating subdir', i
		os.makedirs(i)

######################## USACE DREDGE #############################
# os.chdir(bathy_dir_list[0])
# print 'Current Directory is', os.getcwd()

# #delete python script if it exists
# os.system('[ -e usace_dredge_processing.py ] && rm usace_dredge_processing.py')
# #copy python script from DEM_generation code
# os.system('cp {}/usace_dredge_processing.py usace_dredge_processing.py'.format(code_dir)) 

# print "executing usace_dredge_processing script"
# os.system('python usace_dredge_processing.py {} {}'.format(main_dir, conv_grd_path))
# os.chdir('..')
######################## Multibeam #############################
# os.chdir(bathy_dir_list[1])
# print 'Current Directory is', os.getcwd()

# #delete python script if it exists
# os.system('[ -e mb_processing.py ] && rm mb_processing.py')
# #copy python script from DEM_generation code
# os.system('cp {}/mb_processing.py mb_processing.py'.format(code_dir)) 

# print "executing mb_processing script"
# os.system('python mb_processing.py {} {}'.format(main_dir, name_cell_extents))
# os.chdir('..')
# ####
########################## NOS/BAG ################################
os.chdir(bathy_dir_list[2])
print 'Current Directory is', os.getcwd()

# #delete python script if it exists
os.system('[ -e nos_processing.py ] && rm nos_processing.py')
# #copy python script from DEM_generation code

os.system('cp {}/nos_processing.py nos_processing.py'.format(code_dir)) 

print "executing nos_processing script"
os.system('python nos_processing.py {} {} {}'.format(main_dir,roi_str,conv_grd_path))
os.chdir('..')

#############################################################
# ########################## BATHYTOPO ############################
# #################################################################
# bathytopo_list=[]
# bathytopo_paths=[]

# #################################################################
# ############################# TOPO ##############################
# #################################################################
# bathytopo_list=[]
# bathytopo_paths=[]

# #################################################################
# #################################################################
# #################################################################
# ####################### DATA PROCESSING #########################
# #################################################################
# #################################################################
# #################################################################


# #################################################################
# #################################################################
# #################################################################
# ####################### BATHY SURFACE ###########################
# #################################################################
# #################################################################
# #################################################################



# #################################################################
# #################################################################
# #################################################################
# ####################### DEM GENERATION ##########################
# #################################################################
# #################################################################
# #################################################################

