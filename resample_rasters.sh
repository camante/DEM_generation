mkdir -p one_third
for i in *1_3*.tif;
do
echo $i
echo "Resampling to 1_9th resolution"
#name=${i#*_}
output_tmp="tmp.tif"
output="1_9_tmp_"$i

echo output_tmp is $output_tmp
echo output is $output
#echo $output
gdalwarp -r cubicspline -tr 0.00003086420 0.00003086420 -t_srs EPSG:4269 $i $output_tmp -overwrite

gdal_translate $output_tmp -a_srs EPSG:4269 -a_nodata -99999 -co "COMPRESS=DEFLATE" -co "PREDICTOR=3" -co "TILED=YES" $output
rm $output_tmp
mv $i one_third/$i
echo
done
