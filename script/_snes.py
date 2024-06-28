###############################################################################
#
# SIX PACK by Ragey <i@ragey.net>
# _snes.py
#
# Some helper functions. Note that the SnesToPc and PcToSnes functions are not
# complete and only handle conversions I needed for this project.
#
###############################################################################

import struct

###############################################################################

def SnesToPc(Address, Map = 'fullsa1'):
	if Map == 'fullsa1':
		if ((Address & 0xC00000) == 0xC00000):
			return (Address & 0x3FFFFF) | 0x400000
		if ((Address & 0xC00000) == 0x000000 or (Address & 0xC00000) == 0x800000):
			if ((Address & 0x008000) == 0x000000):
				raise Exception('Cannot convert SnesToPc {:X} ({})'.format(Address, Map))
			return (Address & 0x800000) >> 2 | (Address & 0x3F0000) >> 1 | (Address & 0x7FFF)
		raise Exception('Cannot convert SnesToPc {:X} ({})'.format(Address, Map))
	elif Map == 'lorom':
		return (Address & 0x7FFF) + ((Address & 0x7F0000) >> 1)
	else:
		raise Exception('Not implemented')

def PcToSnes(Address, Map = 'fullsa1'):
	if Map == 'fullsa1':
		if (Address >= 0x800000):
			raise Exception('Cannot convert PcToSnes')
		if ((Address & 0x400000) == 0x400000):
			return Address | 0xC00000
		if ((Address & 0x600000) == 0x000000):
			return ((Address << 1) & 0x3F0000) | 0x8000 | (Address & 0x7FFF)
		if ((Address & 0x600000) == 0x200000):
			return 0x800000 | ((Address << 1) & 0x3F0000) | 0x8000 | (Address & 0x7FFF)
		raise Exception('Cannot convert PcToSnes')
	else:
		raise Exception('Not implemented')

def Make24(Number):
	return struct.pack("BBB", (Number & 0xff), (Number & 0xff00) >> 8, (Number & 0xff0000) >> 16)

def Make16(Number):
	return struct.pack("<H", Number & 0xffff)