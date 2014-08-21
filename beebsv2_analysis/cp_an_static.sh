#!/bin/bash

#Similar to tree-analysis.sh

for dir in ./src/*
do
	[ -d "${dir}" ] || continue
	name="${dir##*/}"
	#echo $dir
	#mkdir ../../beebsv2-analysis-data/$name
	cp $dir/*.analysis.static ../../beebsv2-analysis-data/$name/
done
