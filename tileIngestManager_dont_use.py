#!/usr/bin/env python
#
# --

#--
import sys
import datetime
from osgeo import gdal,osr

Provider="DOC/NOAA/NESDIS/NCEI > National Centers for Environmental Information, NESDIS, NOAA, U.S. Department of Commerce"
Coverage="Topography-Bathymetry; NAVD88"
Today=str(datetime.date.today()).replace("-",":") + " 00:00:00"
##Today="2018:01:09 00:00:00"
NoData=float(-9999)

#--
#
# Mainline
#
#--

if __name__ == "__main__":

    if len(sys.argv) < 2:
        Usage()
        sys.exit()
    else:
        ingrd = sys.argv[1]
        vers = sys.argv[2]

overwrite = True
verbose = True
print >> sys.stderr, "Copying the input file to a properly formatted version"

rast = gdal.Open(ingrd)
georf = rast.GetProjection()
band = rast.GetRasterBand(1)
ginf = rast.GetGeoTransform()
outarray = rast.ReadAsArray()

DEMyear=datetime.date.today()

"""Spatial Resolution is defined by position 1 in list"""
spatRes = ginf[1]
print spatRes
if spatRes <= 0.00003086420:
       res = "19"
elif spatRes == 0.00009259259:
##elif spatRes == 0.000092592592594:
       res = "13"
else:
       res = "99"

"""The upper left coordinates are defined by the list positions 0(X) and 3(Y) respectively"""
Lat = "{0:.2f}".format(ginf[3])
LongAG = ginf[0]
if LongAG < 100:
       Long = "0"+"{0:.2f}".format(ginf[0]*-1)
else:
       Long = "{0:.2f}".format(ginf[0]*-1)

name = str("ncei" + res + "_n" + Lat + "_w" + Long + "_" + DEMyear.strftime('%Y') + "v" + str(vers))
newname = name.replace(".", "x")
print ingrd + "    ----------------->    " + newname + ".tif"

# Create the output GDAL Raster
outfile = newname + ".tif"
(ycount,xcount) = outarray.shape[0],outarray.shape[1]

driver = gdal.GetDriverByName("GTiff")
options = [ 'TILED=YES', 'COMPRESS=DEFLATE', 'PREDICTOR=3' ]
outgeorf = osr.SpatialReference()

dst_ds = driver.Create(outfile, xcount, ycount, 1, gdal.GDT_Float32, options)

if dst_ds is None:
       sys.exit("failed to open output file...%s" %(outfile))

gt = ginf #(xextent,comp_geot[1],0,yextent,0,comp_geot[5])
dst_ds.SetGeoTransform(gt)
dst_ds.SetMetadataItem('TIFFTAG_COPYRIGHT', Provider)
dst_ds.SetMetadataItem('TIFFTAG_IMAGEDESCRIPTION', Coverage)
dst_ds.SetMetadataItem('TIFFTAG_DATETIME', Today)
dst_band = dst_ds.GetRasterBand(1)
dst_ds.SetProjection(georf)
dst_band.SetNoDataValue(NoData)

# Write Numpy Array to the GDAL Raster Band
dst_band.WriteArray(outarray)
dst_band.ComputeStatistics(0)

dst_ds = None
ds = None
