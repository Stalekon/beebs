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

instruction_types = [None]*9

#Memory access instructions
instruction_types[0] = [['adr', 'clrex', 'ldm', 'ldr', 'ldrd', 'ldrex', 'pop',
'push', 'stm', 'str', 'strex','ldrb', 'strh', 'strb', 'ldrh', 'ldmdb','stmib',
'stmia','stmdb', 'ldrsh', 'mov', 'movt', 'movw', 'movs', 'mvns', 'mvn'], 0,
"Memory access instructions"]

#General data processing instructions
instruction_types[1] = [['adc', 'add', 'addw', 'and', 'asr', 'bic', 'clz',
'cmn', 'cmp', 'eor', 'lsl', 'lsr',  'orn', 'orr','rbit', 'rev', 'rev16',
'revsh', 'ror', 'rrx', 'rsb','rsc', 'sadd16', 'sadd8', 'sasx', 'ssax', 'sbc',
'shadd16', 'shadd8', 'shasx', 'shsax', 'shsub16', 'shsub8', 'ssub16', 'ssub8',
'sub', 'subw', 'teq', 'tst', 'uadd16', 'uadd8', 'uasx', 'usax', 'uhadd16',
'uhadd8', 'uhasx', 'uhsax', 'uhsub16', 'uhsub8', 'usad8','usada8', 'usub16',
'usub8', 'adds', 'subs', 'orrs', 'lsrs', 'rsbs', 'ands', 'adcs', 'sbcs',
'lsls', 'rrxs', 'asrs', 'bics', 'rscs'], 0,
"General data processing instructions"]

#Multiply and divide instructions
instruction_types[2] = [['mla', 'mls', 'mul', 'sdiv', 'smla', 'smlad,','smladx'
'smlal', 'smlal', 'smlald','smlaldx' 'smlaw', 'smlsd', 'smlsld', 'smmla',
'smmls','smmlsr', 'smuad','smuadx', 'smul', 'smmul', 'smmulr', 'smull',
'smulwb','smulwt', 'smusd', 'smusdx', 'udiv', 'umaal', 'umlal', 'umull'], 0,
"Multiply and divide instructions"]

#Saturating instructions
instruction_types[3] = [['ssat', 'ssat16', 'usat', 'usat16', 'qadd', 'qsub',
'qsub16', 'qasx', 'qsax', 'qdadd', 'qdsub', 'uqadd16', 'uqadd8', 'uqasx',
'uqsax', 'uqsub16', 'uqsub8'], 0,
"Saturating instructions"]

#Packing and unpacking instructions
instruction_types[4] = [['pkh', 'sxtab', 'sxtab16', 'sxtah', 'sxtb', 'sxtb16',
'sxth', 'uxtab', 'uxtab16', 'uxtah', 'uxtb', 'uxtb16', 'uxth'], 0,
"Packing and unpacking instructions"]

#Bitfield instructions
instruction_types[5] = [['bfc', 'bfi', 'sbfx', 'sxtb', 'sxth', 'ubfx', 'uxtb',
'uxth'], 0,
"Bitfield instructions"]

#Branch and control instructions
instruction_types[6] = [['b', 'bl', 'blx', 'bx', 'cbnz', 'cbz', 'it', 'tbb',
'tbh'], 0,
"Branch and control instructions"]

#Floating-point instructions
instruction_types[7] = [['vabs', 'vadd', 'vcmp', 'vcmpe', 'vcvt',
'vcvtr', 'vcvtb', 'vcvtt', 'vdiv', 'vfma', 'vfnma', 'vfms', 'vfnms',
'vldm', 'vldr', 'vlma', 'vlms', 'vmov', 'vmrs', 'vmsr', 'vmul',
'vneg', 'vnmla', 'vnmls', 'vnmul', 'vpop', 'vpush', 'vsqrt', 'vstm', 'vstr',
'vsub'], 0,
"Floating-point instructions"]

#Miscellaneous instructions
instruction_types[8] = [['bkpt', 'cpsid', 'cpsie', 'dmb', 'dsb', 'isb', 'mrs',
'msr', 'nop', 'sev', 'svc', 'wfe', 'wfi'], 0,
"Miscellaneous instructions"]

condition_siffixes = ['', 'eq', 'ne', 'cs', 'cc', 'mi', 'pl', 'vs', 'vc', 'hi',
'ls', 'ge', 'lt', 'gt', 'le', 'al', 'hs', 'lo']

lenght_suffixes = ['', '.n', '.w']

suffix = [r[0]+r[1] for r in itertools.product(condition_siffixes, lenght_suffixes)]

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
