#!/bin/bash

#Must execute from beebs/build. Beebs must be configured and compiled for avr.

for dir in ./src/*
do
	[ -d "${dir}" ] || continue
	name="${dir##*/}"
	#echo $dir
	for dump in $dir/*.dump.d
	do
		dump_1="${dump##*/}"
		dump_2=(${dump_1//'.'/ })
		dump_name="${dump_2[0]}"
		#echo $dir/${dump_name}
		../analysis/beebsv2_analysis/avr-classify.py -f $dump -d > $dir/$dump_name.analysis.dynamic.avr
	done
done
