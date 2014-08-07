#!/bin/bash

#Must execute from beebs/build. Beebs must be configured and compiled for avr.

for dir in ./src/*
do
	[ -d "${dir}" ] || continue
	name="${dir##*/}"
	#echo $dir
	avr-objdump -d --prefix-addresses $dir/$name > $dir/$name.dump.s
done
