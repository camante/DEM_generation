'''
Description:
-Download lidar with fetch
-Some datasets don't work with fetch. Need to download manually?
-Download by clipping using kirk's methods?
-Convert to nad83, meters vertical
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

if not os.path.exists('raster'):
	os.makedirs('raster')

if not os.path.exists('lidar'):
	os.makedirs('lidar')

main_dir=sys.argv[1]
study_area_shp=sys.argv[2]

#dcfetch.py -R /media/sf_external_hd/al_fl/data/study_area/al_fl_tiles_buff.shp --filter "ID = 8629 or ID = 8668 or ID = 8387 or ID = 8683 or ID = 8616 or ID = 8682 or ID = 6371 or ID = 8567 or ID = 5190 or ID = 5166 or ID = 5169" -x

os.chdir('raster')
print 'Downloading rasters from Digital Coast'
raster_download_cmd='dcfetch.py -R ' + study_area_shp + ' --filter "ID = 8629 or ID = 8668 or ID = 8387 or ID = 8683 or ID = 8616 or ID = 8682 or ID = 6371 or ID = 8567 or ID = 5190 or ID = 5166 or ID = 5169"' 
os.system(raster_download_cmd)
os.chdir('..')


os.chdir('lidar')
print 'Downloading lidar from Digital Coast'
lidar_download_cmd='dcfetch.py -R ' + study_area_shp + ' --filter "ID = 6322 or ID = 5168 or ID = 4924 or ID = 1425"'
os.system(lidar_download_cmd)


















# print "Separating NOS and BAG Surveys"
# move_xyz_gz_cmd="find . -name '*.xyz.gz' -exec mv {} nos_hydro/ \; 2>/dev/null"
# os.system(move_xyz_gz_cmd)

# move_bag_cmd="find . -name '*.bag*' -exec mv {} nos_bag/ \; 2>/dev/null"
# os.system(move_bag_cmd)

# move_bag_gz_cmd="find . -name '*.bag.gz' -exec mv {} nos_bag/ \; 2>/dev/null"
# os.system(move_bag_gz_cmd)

# print "Unzipping NOS"
# os.chdir('nos_hydro')
# os.system('gunzip *.xyz.gz')

# print "Moving all xyz files to xyz directory"
# move_xyz_cmd="find . -name '*.xyz' -exec mv {} xyz/ \; 2>/dev/null"
# os.system(move_xyz_cmd)

# print "Converting NOS to X,Y,Negative Z"
# os.chdir('xyz')
# neg_z_cmd=('nos2xyz.sh')
# os.system(neg_z_cmd)

# print "Converting NOS to NAVD88"
# os.chdir('neg_m')
# nos2navd88_cmd="vert_conv.sh " + conv_grd_path + "  navd88"
# os.system(nos2navd88_cmd)

# print "Creating NOS Datalist"
# os.chdir('navd88')
# nos_datalist_cmd='create_datalist.sh nos'
# os.system(nos_datalist_cmd)

# current_dir=os.getcwd()
# add_to_bmaster_cmd='echo ' + current_dir + '/nos.datalist -1 1 >> ' + main_dir + '/data/bathy_surf/al_fl_bs.datalist' 
# os.system(add_to_bmaster_cmd)
# #add_to_master_cmd='echo ' + current_dir + '/nos.datalist -1 1 >> ' + main_dir + '/software/gridding/al_fl.datalist' 
# #os.system(add_to_master_cmd)
# os.chdir('../../../..')


# os.chdir('nos_bag')

# # print "Converting BAG to Resampled tif and to XYZ"
# # bag2tif2chunks2xyz_cmd='bag2tif2chunks2xyz.sh ' +str(chunk_size) + ' ' + str(resamp_bag) + ' ' + str(resamp_res)
# # os.system(bag2tif2chunks2xyz_cmd)

# print "Converting BAG to NAVD88"
# os.chdir('xyz')
# bag2navd88_cmd="vert_conv.sh " + conv_grd_path + "  navd88"
# os.system(bag2navd88_cmd)

# print "Creating BAG Datalist"
# os.chdir('navd88')
# bag_datalist_cmd='create_datalist.sh bag'
# os.system(bag_datalist_cmd)

# current_dir=os.getcwd()
# add_to_bmaster_cmd='echo ' + current_dir + '/bag.datalist -1 1 >> ' + main_dir + '/data/bathy_surf/al_fl_bs.datalist' 
# os.system(add_to_bmaster_cmd)
# #add_to_master_cmd='echo ' + current_dir + '/bag.datalist -1 1 >> ' + main_dir + '/software/gridding/al_fl.datalist' 
# #os.system(add_to_master_cmd)


