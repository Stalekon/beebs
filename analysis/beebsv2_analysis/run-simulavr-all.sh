#!/bin/bash

#Must execute from beebs/build. Beebs must be configured and compiled for avr.

for dir in ./src/*
do
	[ -d "${dir}" ] || continue
	name="${dir##*/}"
	#echo $dir
	simulavr -d atmega328 -f $dir/$name -v -t $dir/$name.dump.d -g -l 0 &
	proc=$!
	avr-gdb $dir/$name
	kill $proc
done
