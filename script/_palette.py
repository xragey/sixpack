###############################################################################
#
# SIX PACK by Ragey <i@ragey.net>
# _palette.py
#
###############################################################################

import struct

class Palette:
	def __init__(self):
		# first pass
		self.Rows = {}
	
		# second pass
		self.Binary = bytearray()
		self.Dictionary = {}
		self.Count = 0

		# the references to insert
		self.BytesSaved = 0
		self.ReferencedRows = bytearray()

	def Add(self, Binary):
		# Ignore back area color
		Binary = Binary[2:]

		# Set up row references
		for i in range(0, 512, 32):
			Key = str(Binary[i:i+32])
			if Key in self.Rows:
				self.Rows[Key] += 1
			else:
				self.Rows[Key] = 0
	
	def Get(self, Binary):
		NewBinary = bytearray(Binary[:2])
		Binary = Binary[2:]

		for i in range(0, 512, 32):
			Key = str(Binary[i:i+32])
			if Key in self.Dictionary:
				NewBinary += struct.pack("<H", self.Dictionary[Key] | 0x8000)
				self.BytesSaved += 30
			elif self.Rows[Key] > 1:
				self.Dictionary[Key] = len(self.Dictionary)		
				self.ReferencedRows += Binary[i:i+32]
				NewBinary += struct.pack("<H", self.Dictionary[Key] | 0x8000)
				self.BytesSaved -= 2
			else:
				NewBinary += Binary[i:i+32]

		return NewBinary
	
	def GetPaletteRows(self):
		return self.ReferencedRows
