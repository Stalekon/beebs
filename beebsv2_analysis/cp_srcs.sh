#!/bin/bash

#Copy modified sources to beebs/src

for dir in ./src/*
do
	[ -d "${dir}" ] || continue
	name="${dir##*/}"
	cp $dir/*.c ../../src/
done
