#!/usr/bin/env python

import sys

directory = ''
verbose = False
static_analysis = False
raw_data = False
analysis = ''
data_str = " Data"
not_cat = 0

for i,arg in enumerate(sys.argv):
	if 		arg == "-v":
		verbose = True
	elif 	arg == "-s":
		static_analysis = True
		analysis = "Static"
	elif 	arg == "-d":
		static_analysis = False
		analysis = "Dynamic"
	elif 	arg == "-r":
		raw_data = True
		data_str = " Raw" + data_str
	elif 	arg == "-f":
		try:
			directory = sys.argv[i+1]
		except(IndexError):
			directory = ''

if directory == '': sys.exit("No file specified. Use '-f file' to specify a file")
if 	analysis == '': sys.exit("No analysis type specified.\n" +
 "Use -s to analyse output from 'avr-objdump -d --prefix-addresses'\n" \
 "or -d to analyse output from 'simulavr -D -g' up to the halting loop")

def printd(arg,test):
	if (test): print arg

instruction_types = [None]*5

#alu
instruction_types[0] = [["add", "adc", "adiw", "sub", "subi", "sbc", "sbci",
"sbiw", "neg", "inc", "dec", "tst", "clr", "mul", "muls", "mulsu", "fmul",
"fmuls", "fmulsu", "cp", "cpc", "cpi", "and", "andi", "or", "ori", "eor",
"com", "sbr",  "lsl", "lsr", "rol", "ror", "asr", "swap"], 0,
"ALU operations"]

#register
instruction_types[1] = [["mov", "movw", "ldi", "set", "cbr", "cbi", "bset",
"bclr", "bst", "bld", "sec", "clc", "sen", "cln", "sez", "clz", "sei", "cli",
"ses", "cls", "sev", "clv", "set", "clt", "seh", "clh", "sbi"], 0,
"Data movement"]

#memory
instruction_types[2] = [["ld", "ldd", "lds", "st", "std", "sts", "lpm", "spm",
"in", "out", "push", "pop"], 0,
"Memory"]

#control flow
instruction_types[3] = [["rjmp", "ijmp", "jmp", "rcall", "icall", "call",
"ret", "reti", "cpse", "sbrc", "sbrs", "sbic", "sbis", "brbs", "brbc", "breq",
"brne", "brcs", "brcc", "brsh", "brlo", "brmi", "brpl", "brge", "brlt", "brhs",
"brhc", "brts", "brtc", "brvs", "brvc", "brie", "brid"], 0,
"Control Flow"]

#miscellaneous
instruction_types[4] = [["nop", "sleep", "wdr", "break"], 0,
"Miscellaneous"]

#A list where we put the instructions and their count
#The format is ["instruction string", int(count)]
instruction_pool = []

try:
	f = open(directory,'r')
except(IOError):
	sys.exit("Error opening file. Check if file exists.")

for line in f:
	if static_analysis:
		if line[0] != '0':
			continue

		words = line.split()

		try:
			instruction = words[2]
		except:
			continue

	else:
		instruction = line.split()[3].lower()

		if (instruction == "cpu-waitstate"): continue

	for existing_instruction in instruction_pool:
		if (instruction == existing_instruction[0]):
			existing_instruction[1]+=1
			break
	else:
		new_instruction = [instruction, 1]
		instruction_pool.append(new_instruction)

f.close()

instruction_pool.sort()

for ins in instruction_pool:
	for ins_type in instruction_types:
		if ins[0] in ins_type[0]:
			ins_type[1]+=ins[1]
			break
	else:
		not_cat+=1
		printd(ins[0] + " not categorised.", verbose)


top_string = data_str + " from " + analysis + " Analysis "
symbols_len = (52-len(top_string))/2

print "#"*symbols_len + top_string + "#"*symbols_len

print "/"+50*"="+"\\"

if (raw_data):
	for ins in instruction_pool:
		print '> ' + ins[0] + ": " + str(ins[1])
else:
	for ins_type in instruction_types:
		print '> ' + ins_type[2] + ": " + str(ins_type[1])

	print "* Number of segments not categorised: " + str(not_cat)

print "\\"+50*"="+"/"
