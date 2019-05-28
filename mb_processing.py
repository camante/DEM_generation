'''
Description:
-Download MB with fetch
-Process by resampling to X cell size


Author:
Chris Amante
Christopher.Amante@colorado.edu

Date:
5/23/2019

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
######################## MB ###########################
print "Current directory is ", os.getcwd()
main_dir=sys.argv[1]
name_cell_extents=sys.argv[2]
#1 arc-sec
#blkmed_cell=0.00027777777
#1/3 arc-sec res
blkmed_cell=0.000092592596 
print 'Downloading MB Surveys'
mb_download_cmd='download_mb_chunks.sh ' + name_cell_extents + ' '+str(blkmed_cell)
print mb_download_cmd
os.system(mb_download_cmd)

print "Creating datalist"
os.chdir('xyz')

mb_datalist_cmd='create_datalist.sh mb'
os.system(mb_datalist_cmd)

current_dir=os.getcwd()
add_to_bmaster_cmd='echo ' + current_dir + '/mb.datalist -1 1 >> ' + main_dir + '/data/bathy_surf/al_fl_bs.datalist' 
os.system(add_to_bmaster_cmd)
#add_to_master_cmd='echo ' + current_dir + '/mb.datalist -1 1 >> ' + main_dir + '/software/gridding/al_fl.datalist' 
#os.system(add_to_master_cmd)

