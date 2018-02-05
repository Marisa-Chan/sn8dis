#!/usr/bin/python3

import sn8tools.dis
import sn8tools.chips
import sys

def help():
	print("Usage {} cmd:".format(sys.argv[0]))
	print("\tlist   - list MCU names")
	print("\tchip in out [startOffset] [stopOffset] - disassembly file")

if len(sys.argv) == 1:
	help()
elif len(sys.argv) > 1:
	if (sys.argv[1].lower() == "help"):
		help()
	elif (sys.argv[1].lower() == "list"):
		for f in sn8tools.chips.SN8CHIPS.keys():
			print(f)
	elif (len(sys.argv) >= 4):
		f = open(sys.argv[2], "rb")
		a = f.read()
		f.close()
		
		start = -1
		stop = -1
		if len(sys.argv) >= 5:
			start = int(sys.argv[4])
		
		if len(sys.argv) >= 6:
			stop = int(sys.argv[5])
		
		if start < 0:
			if a[:4] == bytes((0x20, 0x20, 0x20, 0x20)):
				a = a[0x100:]
		else:
			if stop > 0:
				a = a[start:stop]
			else:
				a = a[start:]
			
		dis = sn8tools.dis.Disassemble(sys.argv[1], a)
		
		if sys.argv[3] == "--":
			for b in dis:
				print(b)
		else:
			f = open(sys.argv[3], "w")
			for b in dis:
				f.write(b + "\n")
			f.close()
		