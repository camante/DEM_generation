#!/bin/sh
mkdir -p thredds

for i in *.tif;
do
echo "converting tif to nc:" $i
gmt grdconvert $i thredds/$(basename $i .tif).nc -fg -V
done
