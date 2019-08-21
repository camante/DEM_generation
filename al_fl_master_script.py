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
main_dir='/media/sf_external_hd/al_fl'
code_dir='/media/sf_external_hd/al_fl/code/DEM_generation'
name_cell_extents_bs='/media/sf_external_hd/al_fl/data/bathy/bathy_surf/name_cell_extents_bs.csv'
name_cell_extents_dem='/media/sf_external_hd/al_fl/software/gridding/name_cell_extents_dem.csv'
bs_dlist='/media/sf_external_hd/al_fl/data/bathy/bathy_surf/al_fl_bs.datalist'
dem_dlist='/media/sf_external_hd/al_fl/software/gridding/al_fl.datalist'
bs_path='/media/sf_external_hd/al_fl/data/bathy/bathy_surf/tifs'
coast_shp='/media/sf_external_hd/al_fl/data/coast/al_fl_coast'
bs_res=0.00009259259

os.system('cd')
os.chdir(main_dir)

print 'Main Directory is', os.getcwd()
#Creating main subdirectories
dir_list=['data', 'docs', 'software', 'software/gridding']
for i in dir_list:
	if not os.path.exists(i):
		print 'creating subdir', i
		os.makedirs(i)

#Create Empty Dummy BS, Bathy Surface and DEM datalists
create_bs_dlist='''if [ ! -e {}/data/bathy/bathy_surf/al_fl_bs.datalist ] ; 
then touch {}/data/bathy/bathy_surf/al_fl_bs.datalist
fi'''.format(main_dir,main_dir)
os.system(create_bs_dlist)

create_dem_dlist='''if [ ! -e {}/software/gridding/al_fl.datalist ] ; 
then touch {}/software/gridding/al_fl.datalist
fi'''.format(main_dir,main_dir)
os.system(create_dem_dlist)


#ROI for data download
west_buff=-88.525
east_buff=-83.975
south_buff=29.225
north_buff=31.525
roi_str=str(west_buff)+'/'+str(east_buff)+'/'+str(south_buff)+'/'+str(north_buff)
roi_str_ogr=str(west_buff)+' '+str(south_buff)+' '+str(east_buff)+' '+str(north_buff)

#test_ROI
#roi_str=-88.525/-83.975/29.225/31.525
#roi_str='-88.5/-88.49/29.99/30'
#roi_str_ogr='-88.525 29.225 -83.975 31.525'
#roi_str_ogr='-88.5 30.25 -88.25 30.5' 
print "ROI is", roi_str
print "ROI OGR is", roi_str_ogr
#sys.exit()
#shp for digital coast download
study_area_shp=main_dir + '/data/study_area/al_fl_tiles_buff.shp'
#/media/sf_external_hd/al_fl/data/study_area/al_fl_tiles_buff.shp
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

# os.chdir('data/conv_grd')
# print "Creating mllw2navd88 conversion grid"
# conv_grd_cmd='dem cgrid -i mllw -o navd88 -c -E 1s -R' +roi_str
# os.system(conv_grd_cmd)

conv_grd_path=main_dir+'/data/conv_grd/cgrid_mllw2navd88.tif'
#################################################################
#################################################################
#################################################################
####################### DATA DOWNLOAD ###########################
#################################################################
#################################################################
#################################################################

#################################################################
####################### STUDY AREA ##############################
#################################################################
#manually created fishnet shp in Global Mapper (al_fl_tiles.shp) 
#created name_cell_extents with arcpy get_poly_coords.py (name_cell_extents.csv) 
#manually created study area buffer in ArcMap (al_fl_tiles_buff.shp)

#################################################################
######################## COASTLINE ##############################
#################################################################
os.system('cd')
os.chdir(main_dir)
os.chdir('data')

# coast_dir_list=['coast']
# for i in coast_dir_list:
# 	if not os.path.exists(i):
# 		print 'creating subdir', i
# 		os.makedirs(i)

# os.chdir(coast_dir_list[0])

# # #delete python script if it exists
# os.system('[ -e coast_processing.py ] && rm coast_processing.py')
# # #copy python script from DEM_generation code

# os.system('cp {}/coast_processing.py coast_processing.py'.format(code_dir)) 

# print "executing coast_processing script"
# os.system('python coast_processing.py {} {} {}'.format(main_dir,study_area_shp,roi_str_ogr))
# os.chdir('..')

#################################################################
########################## BATHY ################################
#################################################################
os.system('cd')
os.chdir(main_dir+'/data/bathy')

#Creating main subdirectories
# bathy_dir_list=['usace_dredge', 'mb', 'nos']
# #bathy_dir_list=['/media/sf_external_hd/test/usace_dredge']
# for i in bathy_dir_list:
# 	if not os.path.exists(i):
# 		print 'creating subdir', i
# 		os.makedirs(i)

######################## USACE DREDGE #############################
# os.chdir(bathy_dir_list[0])
# print 'Current Directory is', os.getcwd()

# #delete python script if it exists
# os.system('[ -e usace_dredge_processing.py ] && rm usace_dredge_processing.py')
# #copy python script from DEM_generation code
# os.system('cp {}/usace_dredge_processing.py usace_dredge_processing.py'.format(code_dir)) 

# print "executing usace_dredge_processing script"
# os.system('python usace_dredge_processing.py {} {}'.format(main_dir, conv_grd_path))

######################## Multibeam #############################
# os.system('cd')
# os.chdir(main_dir+'/data/bathy')
# os.chdir(bathy_dir_list[1])
# print 'Current Directory is', os.getcwd()

# #delete python script if it exists
# os.system('[ -e mb_processing.py ] && rm mb_processing.py')
# #copy python script from DEM_generation code
# os.system('cp {}/mb_processing.py mb_processing.py'.format(code_dir)) 

# print "executing mb_processing script"
# os.system('python mb_processing.py {} {}'.format(main_dir, name_cell_extents))
# ####
########################## NOS/BAG ################################
# os.system('cd')
# os.chdir(main_dir+'/data/bathy')
# os.chdir(bathy_dir_list[2])
# print 'Current Directory is', os.getcwd()

# # #delete python script if it exists
# os.system('[ -e nos_processing.py ] && rm nos_processing.py')
# # #copy python script from DEM_generation code

# os.system('cp {}/nos_processing.py nos_processing.py'.format(code_dir)) 

# print "executing nos_processing script"
# os.system('python nos_processing.py {} {} {}'.format(main_dir,roi_str,conv_grd_path))

#############################################################
################## DIGITAL COAST LIDAR ######################
#############################################################
os.system('cd')
os.chdir(main_dir+'/data')

dc_lidar_dir_list=['dc_lidar']
for i in dc_lidar_dir_list:
	if not os.path.exists(i):
		print 'creating subdir', i
		os.makedirs(i)

os.chdir(dc_lidar_dir_list[0])

# #delete python script if it exists
os.system('[ -e dc_lidar_processing.py ] && rm dc_lidar_processing.py')
# #copy python script from DEM_generation code

os.system('cp {}/dc_lidar_processing.py dc_lidar_processing.py'.format(code_dir)) 

print "executing dc_lidar_processing script"
os.system('python dc_lidar_processing.py {} {}'.format(main_dir,study_area_shp))


os.system('cd')
os.chdir(main_dir+'/data/dc_lidar')

dc_lidar_missing_dir_list=['missing']
for i in dc_lidar_missing_dir_list:
	if not os.path.exists(i):
		print 'creating subdir', i
		os.makedirs(i)


os.chdir(dc_lidar_missing_dir_list[0])

# #delete python script if it exists
os.system('[ -e dc_lidar_missing_processing.py ] && rm dc_lidar_missing_processing.py')
# #copy python script from DEM_generation code

os.system('cp {}/dc_lidar_missing_processing.py dc_lidar_missing_processing.py'.format(code_dir)) 

print "executing dc_lidar_missing_processing script"
os.system('python dc_lidar_missing_processing.py {}'.format(main_dir))


#############################################################
################## TOPO NOT ON DIGITAL COAST ################
#############################################################
# os.system('cd')
# os.chdir(main_dir+'/data')

# dc_lidar_dir_list=['dc_lidar']
# for i in dc_lidar_dir_list:
# 	if not os.path.exists(i):
# 		print 'creating subdir', i
# 		os.makedirs(i)

# os.chdir(dc_lidar_dir_list[0])

# # #delete python script if it exists
# os.system('[ -e dc_lidar_processing.py ] && rm dc_lidar_processing.py')
# # #copy python script from DEM_generation code

# os.system('cp {}/dc_lidar_processing.py dc_lidar_processing.py'.format(code_dir)) 

# print "executing dc_lidar_processing script"
# os.system('python dc_lidar_processing.py {} {}'.format(main_dir,study_area_shp))
# os.chdir('..')


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
# os.system('cd')
# os.chdir(main_dir+'/data/bathy')

# #Create Bathy Surface 
# if not os.path.exists('bathy_surf'):
# 	os.makedirs('bathy_surf')

# os.chdir('bathy_surf')
# bathy_surf_cmd='create_bs.sh ' + name_cell_extents_bs + ' ' + bs_dlist + ' ' + coast_shp + ' ' + bs_res
# #create_bs.sh /media/sf_external_hd/al_fl/data/bathy/bathy_surf/name_cell_extents_bs.csv /media/sf_external_hd/al_fl/data/bathy/bathy_surf/al_fl_bs.datalist /media/sf_external_hd/al_fl/data/coast/al_fl_coast 0.00009259259
# #create_bs.sh name_cell_extents_test.csv /media/sf_external_hd/al_fl/data/bathy/bathy_surf/al_fl_bs.datalist /media/sf_external_hd/al_fl/data/coast/al_fl_coast 0.00009259259
# os.system(bathy_surf_cmd)

# #################################################################
# #################################################################
# #################################################################
# ####################### DEM GENERATION ##########################
# #################################################################
# #################################################################
# #################################################################
# #Create DEM
# os.system('cd')
# os.chdir(main_dir)
# os.chdir('software/gridding')

# create_dem_cmd='create_dem.sh ' + name_cell_extents_dem + ' ' + dem_dlist + ' ' + bs_path + ' ' + str(5)
# #create_dem.sh /media/sf_external_hd/al_fl/software/gridding/name_cell_extents_dem.csv /media/sf_external_hd/al_fl/software/gridding/al_fl.datalist /media/sf_external_hd/al_fl/data/bathy/bathy_surf/tifs 5
#create_dem.sh /media/sf_external_hd/al_fl/software/gridding/name_cell_extents_dem.csv /media/sf_external_hd/al_fl/software/gridding/al_fl.datalist 5
# os.system(bathy_surf_cmd)
