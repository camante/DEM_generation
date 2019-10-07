#!/bin/sh

file=$1

gdal_translate ${file} -of netCDF $(basename ${file} .tif).nc
grdedit -T $(basename ${file} .tif).nc

