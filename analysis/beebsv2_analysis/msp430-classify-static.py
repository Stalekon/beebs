#!/usr/bin/env python

import sys
import itertools

directory = ''
verbose = False
not_cat = 0

for i,arg in enumerate(sys.argv):
	if 		arg == "-v": verbose = True
	elif arg == "-f":
		try:
			directory = sys.argv[i+1]
		except(IndexError):
			directory = ''


if directory == '': sys.exit("No file specified. Use '-f file' to specify a file")

instruction_types = [None]*4

#Arithmetic and Logic
instruction_types[0] = [['add', 'addc', 'and', 'bic', 'bis', 'bit', 'cmp',
'dadd', 'xor', 'sub', 'subc', 'adc', 'dadc', 'dec', 'decd', 'inc', 'incd',
'sbc', 'inv'], 0,
"Arithmetic and Logic"]

#Branch instructions
instruction_types[1] = [['jc', 'jhs', 'jeq', 'jz', 'jge', 'jl', 'jmp', 'jn',
'jnc', 'jlo', 'jne', 'jnz', 'call', 'reti', 'br', 'dint', 'eint', 'nop',
'ret'], 0,
"Branch instructions"]

#Data transfer
instruction_types[2] = [['mov', 'push', 'clr', 'clrc', 'clrn', 'clrz', 'pop',
'setc', 'setn', 'setz', 'tst'], 0,
"Data transfer"]

#Bit operations
instruction_types[3] = [['rra', 'rrc', 'rla', 'rlc', 'rru', 'swpb', 'sxt'], 0,
"Bit operations"]

misc_suffixes = ['', 'm', 'a']

lenght_suffixes = ['', '.b', '.w']

suffix = [r[0]+r[1] for r in itertools.product(misc_suffixes, lenght_suffixes)]

try:
	f = open(directory,'r')
except(IOError):
	sys.exit("Error opening file. Check if file exists.")

for line in f:
	words = line.split()
	try:
		instruction = words[2]
	except:
		continue

	is_cathegorised = False

	for ins_type in instruction_types:
		for element in ins_type[0]:
			if (instruction.startswith(element) and
				instruction[len(element):] in suffix):
				ins_type[1]+=1
				is_cathegorised = True
				break
			if (is_cathegorised): break

	if (not is_cathegorised): not_cat+=1

	if (not is_cathegorised and verbose):
		print instruction + " was not categorised"

f.close()

print "/"+50*"="+"\\"

for ins_type in instruction_types:
	print ins_type[2] + ": " + str(ins_type[1])

print "Number of segments not categorised: " + str(not_cat)

print "\\"+50*"="+"/"
