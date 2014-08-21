#!/usr/bin/env python

import sys
import itertools

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

static_analysis = True

def printd(arg,test):
	if (test): print arg

instruction_types = [None]*5

#alu
instruction_types[0] = [["mov", "movs", "add", "adds", "adcs", "adr", "subs",
"sub", "sbcs", "adc", "sbc", "rsbs", "muls", "cmp", "cmn", "ands", "eors",
"orrs", "mvns", "bics", "tst", "lsls", "lsrs", "asrs", "rors", "sxth", "sxtb",
"uxth", "uxtb", "rev", "rev16", "revsh"], 0,
"ALU operations"]

#register
instruction_types[1] = [[], 0,
"Data movement"]

#memory
instruction_types[2] = [["ldr", "ldrh", "ldrsh", "ldrsb", "ldm", "str",
"strh", "strb", "stm", "push", "pop"], 0,
"Memory"]

#control flow
instruction_types[3] = [["b", "beq", "bne", "bcs", "bcc", "bmi", "bpl",
"bvs", "bvc", "bhi", "bls", "bge", "blt", "bgt", "ble", "bl", "bx", "blx"], 0,
"Control Flow"]

#miscellaneous
instruction_types[4] = [["svc", "cpsid", "cpsie", "mrs", "msr", "bkpt",
"sev", "wfe", "wfi", "yeild", "nop", "isb", "dmb", "dsb"], 0,
"Miscellaneous"]

condition_siffixes = ['', 'eq', 'ne', 'cs', 'cc', 'mi', 'pl', 'vs', 'vc', 'hi',
'ls', 'ge', 'lt', 'gt', 'le', 'al', 'hs', 'lo']

lenght_suffixes = ['', '.n', '.w']

suffixes = [r[0]+r[1] for r in itertools.product(condition_siffixes, lenght_suffixes)]


#A list where we put the instructions and their count
#The format is ["instruction string", int(count)]
instruction_pool = []

try:
	f = open(directory,'r')
except(IOError):
	sys.exit("Error opening file. Check if file exists. " + directory)

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

for instruction in instruction_pool:
	for ins_type in instruction_types:
		for element in ins_type[0]:
			if (instruction[0].startswith(element))	and\
			(instruction[0][len(element):] in suffixes):
				ins_type[1]+=instruction[1]
				break
		else:
			continue
		break
	else:
		not_cat+=1
		printd(instruction[0] + " not categorised.", verbose)


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
