#!/bin/sh
function help () {
echo "pos2neg_ft2m- Script that converts third column in xyz file from positive to negative and feet to meter by multiply by -0.3048"
	echo "Usage: $0 extension delim "
	echo "* extension: extension, Example: .csv or .xyz"
	echo "* delim: delimiter, if not provided then space is assumed"
}

extension=$1
delim=$2

if [ "$delim" == "" ]
then
	echo
	echo "IMPORTANT:"
	echo "User did not provide delimiter information. Assuming space, output will be incorrect if not actually space."
	echo
	param=""
else
	echo "User input delimiter is NOT space. Taking delimiter from user input"
	param="-F"$delim
fi

total_files=$(ls -lR *$extension | wc -l)

echo "Total number of xyz files to process:" $total_files
file_num=1

mkdir -p neg_m


for i in *$extension;
do
echo "Processing File" $file_num "out of" $total_files
echo "File name is " $i
awk $param '{printf "%.8f %.8f %.3f\n", $1,$2,$3*-0.3048}' $i > "neg_m/"$(basename $i $extension)"_neg_m.xyz"
echo

file_num=$((file_num + 1))
done

