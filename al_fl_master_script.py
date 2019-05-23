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
import glob
#################################################################
#################################################################
#################################################################
###################### INITIAL VARIABLES ########################
#################################################################
#################################################################
#################################################################
#set main working directory
main_dir='/media/sf_external_hd/al_fl'
os.chdir(main_dir)
print 'Main Directory is', os.getcwd()
#Creating main subdirectories
dir_list=['data', 'docs', 'software']
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

#os.chdir('data/conv_grd')
#print "Creating mllw2navd88 conversion grid"
#conv_grd_cmd='dem cgrid -i mllw -o navd88 -E 1s -R' +roi_str
#os.system(conv_grd_cmd)

conv_grd_path=main_dir+'data/conv_grd/'

#################################################################
#################################################################
#################################################################
####################### DATA DOWNLOAD ###########################
#################################################################
#################################################################
#################################################################
os.chdir('data')

#################################################################
####################### STUDY AREA ##############################
#################################################################
#manually created fishnet shp in Global Mapper (al_fl_tiles.shp) 
#created name_cell_extents with arcpy get_poly_coords.py (name_cell_extent.csv) 
#manually created study area buffer in ArcMap (al_fl_tiles_buff.shp)

#################################################################
######################## COASTLINE ##############################
#################################################################

#################################################################
########################## BATHY ################################
#################################################################
#Creating main subdirectories
bathy_dir_list=['bathy/usace_dredge']
for i in bathy_dir_list:
	if not os.path.exists(i):
		print 'creating subdir', i
		os.makedirs(i)

########################## NOS/BAG ################################
#Requested NOS/BAG Files from Lee Shoemaker

######################## USACE DREDGE #############################
#Download USACE with fetch
os.chdir(bathy_dir_list[0])
print 'Current Directory is', os.getcwd()

if not os.path.exists('zip'):
	os.makedirs('zip')

if not os.path.exists('gdb'):
	os.makedirs('gdb')

if not os.path.exists('xyz'):
	os.makedirs('xyz')

#print 'Downloading USACE Channel Surveys'
#usace_download_cmd='usacefetch.py -R ' +roi_str
#os.system(usace_download_cmd)

#Move all zip files to zip dir
move_zip_cmd="find . -name '*.zip' -exec mv {} /zip \;"
os.system(move_zip_cmd)
move_zip_cmd="find . -name '*.ZIP' -exec mv {} /zip \;"
os.system(move_zip_cmd2)

#unzip all zip files
os.chdir('zip')
unzip_cmd='unzip "*.zip"'
os.system(unzip_cmd)
unzip_cmd2='unzip "*.ZIP"'
os.system(unzip_cmd2)

#Move all gdb files to gdb dir
os.chdir(bathy_dir_list[0])
move_gdb_cmd="find . -name '*.gdb' -exec mv {} /gdb \;"
os.system(move_gdb_cmd)

#Convert all gdb to shapefile, reproject to nad83, and convert pos ft to neg m
#try first creating it from SurveyPoint_HD, if that doesn't exist, use SurveyPoint.
#if SurveyPoint doesn't exist, print name to text file to investigate


# COMMENTED OUT BELOW



# os.chdir('gdb')
# for i in glob.glob("*.gdb"):
# 	print "Processing File", i
# 	gdb_basename = i[:-4]
# 	#create SurveyPoint_HD or SurveyPoint shp
# 	try:
# 		create_usace_shp_cmd ='ogr2ogr -f "ESRI Shapefile" %s %s SurveyPoint_HD' % (gdb_basename i)
# 		os.call(create_usace_shp_cmd)
# 		os.chdir(gdb_basename)
# 		sp2nad83_cmd ='ogr2ogr -f "ESRI Shapefile" -t_srs EPSG:4269 %s_nad83.shp %s.shp' % (gdb_basename gdb_basename)
# 		os.call(sp2nad83_cmd)
# 		shp2csv_cmd = 'ogr2ogr -f "CSV" %s_nad83.csv %s_nad83.shp -lco GEOMETRY=AS_XY -select "Z_depth"' % (gdb_basename)
# 		os.call(shp2csv_cmd)
# 		os.call('%s >> gdb_surveypoints_HD.txt' % (gdb_basename))
# 	except:
# 		try:
# 			create_usace_shp_cmd2='ogr2ogr -f "ESRI Shapefile" %s %s SurveyPoint' % (gdb_basename i)
# 			os.call(create_usace_shp_cmd2)
# 			os.chdir(gdb_basename)
# 			sp2nad83_cmd2 ='ogr2ogr -f "ESRI Shapefile" -t_srs EPSG:4269 %s_nad83.shp %s.shp' % (gdb_basename gdb_basename)
# 			os.call(sp2nad83_cmd2)
# 			shp2csv_cmd2 = 'ogr2ogr -f "CSV" %s_nad83.csv %s_nad83.shp -lco GEOMETRY=AS_XY -select "Z_depth"' % (gdb_basename)
# 			os.call(shp2csv_cmd2)
# 			os.call('%s >> gdb_no_surveypoints_HD.txt' % (gdb_basename))
# 		except:
# 			os.call('%s >> gdb_no_surveypoints.txt' % (gdb_basename))

# 	# ogr2ogr -f "ESRI Shapefile" SurveyPoint BC_01_BCN_20120517_CS.gdb SurveyPoint
# 	# ogr2ogr -f "ESRI Shapefile" SurveyPoint_HD BC_01_BCN_20120517_CS.gdb SurveyPoint_HD
# 	# #convert shp to nad83
# 	# ogr2ogr -f "ESRI Shapefile" -t_srs EPSG:4269 test_nad83.shp SurveyPoint.shp
# 	# #convert shp to xyz
# 	# ogr2ogr -f "CSV" -overwrite test_nad83.csv test_nad83.shp -lco GEOMETRY=AS_XY -select "Z_depth"
# 	# #remove header, covert xyz from feet to meters, positive to neg
# 	# #ft2m_cmd=awk -F, '{if (NR!=1) {printf "%.8f %.8f %.3f\n", $1,$2,$3*-0.3048}}' test_nad83.csv > test_nad83_neg_m.xyz


# #Move all xyz files to xyz dir
# move_xyz_cmd="find . -name '*nad83_neg_m.xyz' -exec mv {} /xyz \;"
# os.system(move_xyz_cmd)

# #convert xyz from mllw to navd88
# os.chdir('xyz')
# usace_vert_conv_cmd='vert_conv.sh navd88 '+conv_grd_path
# os.system(usace_vert_conv_cmd)

# #create datalist
# os.chdir('navd88')
# usace_datalist_cmd='create_datalist.sh usace_dredge'
# os.system(usace_datalist_cmd)

# #################################################################
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

