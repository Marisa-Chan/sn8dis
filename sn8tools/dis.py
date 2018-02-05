import sn8tools.chips
import sys

def prntOp1(fmt, op, chip):
	return fmt.format(op & 0xFF)

def prntBit(fmt, op, chip):
	return fmt.format(op & 0xFF, (op >> 8) & 7)

def prntB0X(fmt, op, chip):
	return fmt.format( chip.getRegName(op & 0xFF) )

def prntB0X2(fmt, op, chip):
	return fmt.format( chip.getRegName( ((op >> 8) & 7) + 0x80 ) , op & 0xFF)
	
def prntB0XBit(fmt, op, chip):
	return fmt.format( chip.getRegName(op & 0xFF) , (op >> 8) & 7)

def prntAddr(fmt, op, chip):
	return fmt.format(op & 0x3FFF)

def prntNone(fmt, op, chip):
	return fmt

AsmForm = dict((
("MOV_A_BX_RD",			("MOV A, 0x{:02X}",	prntOp1)),
("MOV_BX_WR_A",			("MOV 0x{:02X}, A",	prntOp1)),
("B0XCH_A_B0_RW",		("B0XCH A, {}",		prntB0X)),
("B0XCH_A_B0_RW_No80FF",	("B0XCH A, {}",		prntB0X)),
("MOVC_None_None",		("MOVC",		prntNone)),
("ADC_A_BX_RD",			("ADC A, 0x{:02X}",	prntOp1)),
("ADC_BX_RW_A",			("ADC 0x{:02X}, A",	prntOp1)),
("ADD_A_BX_RD",			("ADD A, 0x{:02X}",	prntOp1)),
("ADD_BX_RW_A",			("ADD 0x{:02X}, A",	prntOp1)),
("B0ADD_B0_RW_A",		("B0ADD {}, A",		prntB0X)),
("ADD_A_CONST",			("ADD A, #{:02X}h",	prntOp1)),
("DAA_None_None",		("DAA",			prntNone)),
("DAA_2X_None_None",		("DAA",			prntNone)),
("OR_A_BX_RD",			("OR A, 0x{:02X}",	prntOp1)),
("OR_BX_RW_A",			("OR 0x{:02X}, A",	prntOp1)),
("OR_A_CONST",			("OR A, #{:02X}h",	prntOp1)),
("XOR_A_BX_RD",			("XOR A, 0x{:02X}",	prntOp1)),
("XOR_BX_RW_A",			("XOR 0x{:02X}, A",	prntOp1)),
("XOR_A_CONST",			("XOR A, #{:02X}h",	prntOp1)),
("SWAP_BX_RD_None",		("SWAP 0x{:02X}",	prntOp1)),
("RRC_BX_RD_None",		("RRC 0x{:02X}",	prntOp1)),
("RRCM_BX_RW_None",		("RRCM 0x{:02X}",	prntOp1)),
("RLC_BX_RD_None",		("RLC 0x{:02X}",	prntOp1)),
("RLCM_BX_RW_None",		("RLCM 0x{:02X}",	prntOp1)),
("CMPRS_A_CONST",		("CMPRS A, #{:02X}h",	prntOp1)),
("CMPRS_A_BX_RD",		("CMPRS A, 0x{:02X}",	prntOp1)),
("INCS_BX_RD_None",		("INCS 0x{:02X}",	prntOp1)),
("INCMS_BX_RW_None",		("INCMS 0x{:02X}",	prntOp1)),
("RET_None_None",		("RET",			prntNone)),
("RETI_None_None",		("RETI",		prntNone)),
("NOP_None_None",		("NOP",			prntNone)),
("PUSH_None_None",		("PUSH",		prntNone)),
("POP_None_None",		("POP",			prntNone)),
("ROMWRT_None_None",		("ROMWRT",		prntNone)),
("B0MOV_A_B0_RD",		("B0MOV A, {}",		prntB0X)),
("B0MOV_B0_WR_A",		("B0MOV {}, A",		prntB0X)),
("MOV_A_CONST",			("MOV A, #{:02X}h",	prntOp1)),
("B0MOV_U87_CONST",		("B0MOV {}, #{:02X}h",	prntB0X2)),
("B0MOV_U87_CONST_NoE6E7",	("B0MOV {}, #{:02X}h",	prntB0X2)),
("B0MOV_U87_A",			("B0MOV {}, A",		prntB0X)),
("XCH_A_BX_RW",			("XCH A, 0x{:02X}",	prntOp1)),
("SBC_A_BX_RD",			("SBC A, 0x{:02X}",	prntOp1)),
("SBC_BX_RW_A",			("SBC 0x{:02X}, A",	prntOp1)),
("SUB_A_BX_RD",			("SUB A, 0x{:02X}",	prntOp1)),
("SUB_BX_RW_A",			("SUB 0x{:02X}, A",	prntOp1)),
("SUB_A_CONST",			("SUB A, #{:02X}h",	prntOp1)),
("MUL_A_BX_RD",			("MUL A, 0x{:02X}",	prntOp1)),
("AND_A_BX_RD",			("AND A, 0x{:02X}",	prntOp1)),
("AND_BX_RW_A",			("AND 0x{:02X}, A",	prntOp1)),
("AND_A_CONST",			("AND A, #{:02X}h",	prntOp1)),
("SWAPM_BX_RW_None",		("SWAPM 0x{:02X}",	prntOp1)),
("CLR_BX_WR_None",		("CLR 0x{:02X}",	prntOp1)),
("BCLR_BITX_RW_None",		("BCLR 0x{:02X}.{:d}",	prntBit)),
("BSET_BITX_RW_None",		("BSET 0x{:02X}.{:d}",	prntBit)),
("B0BCLR_BIT0_RW_None",		("B0BCLR {}.{:d}",	prntB0XBit)),
("B0BSET_BIT0_RW_None",		("B0BSET {}.{:d}",	prntB0XBit)),
("DECS_BX_RD_None",		("DECS 0x{:02X}",	prntOp1)),
("DECMS_BX_RW_None",		("DECMS 0x{:02X}",	prntOp1)),
("BTS0_BITX_RD_None",		("BTS0 0x{:02X}.{:d}",	prntBit)),
("BTS1_BITX_RD_None",		("BTS1 0x{:02X}.{:d}",	prntBit)),
("B0BTS0_BIT0_RD_None",		("B0BTS0 {}.{:d}",	prntB0XBit)),
("B0BTS1_BIT0_RD_None",		("B0BTS1 {}.{:d}",	prntB0XBit)),
("CALLHL_None_None",		("CALLHL",		prntNone)),
("CALLYZ_None_None",		("CALLYZ",		prntNone)),
("JMP_ADR_ABS_None",		("JMP 0x{:04X}",	prntAddr)),
("CALL_ADR_ABS_None",		("CALL 0x{:04X}",	prntAddr)),
("RETLW_CONST_None",		("RETLW 0x{:04X}",	prntOp1)),
("COM_BX_RD_None",		("COM 0x{:02X}",	prntOp1)),
("COMM_BX_RW_None",		("COMM 0x{:02X}",	prntOp1)),
("INC_BX_RD_None",		("INC 0x{:02X}",	prntOp1)),
("INCM_BX_RW_None",		("INCM 0x{:02X}",	prntOp1)),
("DEC_BX_RD_None",		("DEC 0x{:02X}",	prntOp1)),
("DECM_BX_RW_None",		("DECM 0x{:02X}",	prntOp1)),
("TS0M_BX_RD_None",		("TS0M 0x{:02X}",	prntOp1))
))


Identifer = ((
(0x1e00, 0xff00), (0x1f00, 0xff00), (0x0200, 0xff00), (0x0d00, 0xff00), (0x0100, 0xff00), (0x1000, 0xff00), (0x1100, 0xff00), (0x1200, 0xff00),
(0x1300, 0xff00), (0x0300, 0xff00), (0x1400, 0xff00), (0x0c66, 0xffff), (0x0c00, 0xffff), (0x1800, 0xff00), (0x1900, 0xff00), (0x1a00, 0xff00),
(0x1b00, 0xff00), (0x1c00, 0xff00), (0x1d00, 0xff00), (0x1700, 0xff00), (0x0800, 0xff00), (0x0900, 0xff00), (0x0a00, 0xff00), (0x0b00, 0xff00),
(0x0600, 0xff00), (0x0700, 0xff00), (0x1500, 0xff00), (0x1600, 0xff00), (0x0e00, 0xff00), (0x0f00, 0xff00), (0x0000, 0xffff), (0x0400, 0xff00),
(0x0500, 0xff00), (0x0400, 0xff00), (0x0500, 0xff00), (0x0100, 0xff00)
),(
(0x2e00, 0xff00), (0x2f00, 0xff00), (0x2d00, 0xff00), (0x3000, 0xf800), (0x2f80, 0xff80), (0x2c00, 0xff00), (0x2000, 0xff00), (0x2100, 0xff00),
(0x2200, 0xff00), (0x2300, 0xff00), (0x2400, 0xff00), (0x3800, 0xff00), (0x2800, 0xff00), (0x2900, 0xff00), (0x2a00, 0xff00), (0x2700, 0xff00),
(0x2b00, 0xff00), (0x4000, 0xf800), (0x4800, 0xf800), (0x6000, 0xf800), (0x6800, 0xf800), (0x2500, 0xff00), (0x2600, 0xff00), (0x5000, 0xf800),
(0x5800, 0xf800), (0x7000, 0xf800), (0x7800, 0xf800), (0x3a00, 0xff00), (0x3c00, 0xff00), (0x3c00, 0xff00), (0x3d00, 0xff00), (0x8000, 0xc000),
(0xc000, 0xc000), (0x3f00, 0xff00), (0x3900, 0xff00), (0x3a00, 0xff00), (0x3b00, 0xff00), (0x3e00, 0xff00)
))


def OpCheck(opcode):
	lst = None
	if (opcode & 0xE000):
		lst = Identifer[1]
	else:
		lst = Identifer[0]
	for a in lst:
		if a[0] == a[1] & opcode:
			return (1, a[0])
	return (0, opcode)

def DecodeWord(chip, val):
	(r, op) = OpCheck(val)
	if (r == 1):
		if op in chip.codes:
			sn8op = chip.codes[op]
			if sn8op.name not in AsmForm:
				sys.stderr.write("Unknown 0x{:04X} --> {}!\n".format(val, sn8op.name))
			else:
				asm = AsmForm[sn8op.name]
				return (1, asm[1](asm[0], val & sn8op.datmask, chip))

	return (0, "?????") #"{:04X}".format(val)

def DecodeDword(chip, val):
	if chip.adv != None:
		for op in chip.adv:
			if op.sz == 4:
				if ((val & op.opmask) == op.opcode):
					return (1, op.decode(val & op.datmask))

	return (0, "?????")

def Disassemble(chipName, data):
	lst = list()
	if chipName.upper() not in sn8tools.chips.SN8CHIPS:
		lst.append("Unknown chip {}".format(chipName))
		return lst
	
	chip = sn8tools.chips.SN8CHIPS[ chipName.upper() ]
	
	i = 0
	maxln = (len(data) & (~1))
	while i < maxln:
		sz = 2
		word = int.from_bytes(data[i:i+2], "little")
		
		(succ, asmCode) = DecodeWord(chip, word)
		s = "{: 5X}: {:04X}       \t{}".format(i // 2, word, asmCode)
		
		if (succ == 0 and maxln - i >= 4 and chip.adv != None):
			dword = (int.from_bytes(data[i:i+2], "little") << 16) | int.from_bytes(data[i+2:i+4], "little")
			(succ, asmCode2) = DecodeDword(chip, dword)
			if ( succ == 1 ):
				sz = 4
				s = "{: 5X}: {:08X}   \t{}".format(i // 2, dword, asmCode2)

		lst.append(s)
		
		i += sz
		
	return lst

