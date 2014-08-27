#!/bin/bash

#Must execute from beebs/build. Beebs must be configured and compiled for avr.

for dir in ./src/*
do
	[ -d "${dir}" ] || continue
	name="${dir##*/}"
	#echo $dir
	for dump in $dir/*.dump_*.d
	do
		dump_1="${dump##*/}"
		dump_2=(${dump_1//'.'/ })
		dump_name="${dump_2[0]}"
		#echo $dir/${dump_name}
		cat $dump >> $dir/$dump_name.dump.d
	done
done
