###############################################################################
#
# SIX PACK by Ragey <i@ragey.net>
# _smw.py
#
# Class represents either a SMW image or a Six Pack image.
#
###############################################################################

import random
import struct
from _snes import *

###############################################################################

class SuperMarioWorld():
	def __init__(self, Path):
		self.Path = Path
		self.Verbose = '\n\n{}\n'.format(self.Path)
		self.Default = True

		with open(Path, 'rb') as File:
			self.Binary = bytearray(File.read())

		# Remove copier header
		Header = len(self.Binary) % 32768
		self.Binary = self.Binary[Header:]

		self.Mapper = 'fullsa1' if self.Binary[SnesToPc(0xFFD5)] == 0x23 else 'lorom'
		
		# Indirect pointer to ExAnimation data
		ExAnimIndirect = SnesToPc(int.from_bytes(self.Binary[SnesToPc(0x0583ae, self.Mapper):SnesToPc(0x0583ae, self.Mapper)+3], byteorder = 'little', signed = False), self.Mapper) + 234

		# Data pointers
		self.Layer1Pointers      = SnesToPc(0x05e000, self.Mapper)
		self.Layer2Pointers      = SnesToPc(0x05e600, self.Mapper)
		self.SpritePointers      = SnesToPc(0x05ec00, self.Mapper)
		self.PalettePointers     = SnesToPc(0x0ef600, self.Mapper)
		self.StageHeader03FE00   = SnesToPc(0x03fe00, self.Mapper)
		self.StageHeader05F000   = SnesToPc(0x05f000, self.Mapper)
		self.StageHeader05F200   = SnesToPc(0x05f200, self.Mapper)
		self.StageHeader05F400   = SnesToPc(0x05f400, self.Mapper)
		self.StageHeader05F600   = SnesToPc(0x05f600, self.Mapper)
		self.StageHeader05DE00   = SnesToPc(0x05de00, self.Mapper)
		self.StageHeader06FC00   = SnesToPc(0x06fc00, self.Mapper)
		self.StageHeader06FE00   = SnesToPc(0x06fe00, self.Mapper)
		self.SpriteBanks         = SnesToPc(0x0ef100, self.Mapper)
		self.StageHeader0EF310   = SnesToPc(0x0ef310, self.Mapper)
		self.LevelNames          = SnesToPc(int.from_bytes(self.Binary[SnesToPc(0x03bb57, self.Mapper):SnesToPc(0x03bb57, self.Mapper)+3], byteorder = 'little', signed = False), self.Mapper)
		self.StageGraphicsBypass = SnesToPc(int.from_bytes(self.Binary[SnesToPc(0x0ff7ff, self.Mapper):SnesToPc(0x0ff7ff, self.Mapper)+3], byteorder = 'little', signed = False), self.Mapper)
		self.MessagePointers     = SnesToPc(0x03be80, self.Mapper)
		self.Messages            = SnesToPc(int.from_bytes(self.Binary[SnesToPc(0x03bc0b, self.Mapper):SnesToPc(0x03bc0b, self.Mapper)+3], byteorder = 'little', signed = False), self.Mapper)
		self.ContestNumbers      = SnesToPc(0x0cd500, self.Mapper)
		self.AuthorNames         = SnesToPc(0x0c9000, self.Mapper)
		self.PaletteRows         = SnesToPc(0xc33000, self.Mapper)
		self.DemoReel            = SnesToPc(0x0df300, self.Mapper)
		self.StageExAnimPointers = SnesToPc(int.from_bytes(self.Binary[ExAnimIndirect:ExAnimIndirect+3], byteorder = 'little', signed = False), self.Mapper)
		self.Gfx33Identifiers    = SnesToPc(0x01ffc0, self.Mapper)
		self.Gfx33Users          = SnesToPc(0x01ffe0, self.Mapper)
		self.Gfx33Index          = 0
		self.CustomMLIndex       = 1 # first index is for default palettes
		self.CustomMLPalette     = SnesToPc(0xffe000, self.Mapper) + 80 # first index is default palettes

		# Ugly hack, the entries are not SA1 images and SixPack and the Segments are
		# Proper way would be to detect if the Lunar Magic secondary entrances hijack has been installed
		if self.Mapper == 'fullsa1':
			self.Secondary05F800     = SnesToPc(int.from_bytes(self.Binary[SnesToPc(0x0de191, self.Mapper):SnesToPc(0x0de191, self.Mapper)+3], byteorder = 'little', signed = False), self.Mapper)
			self.Secondary05FA00     = SnesToPc(int.from_bytes(self.Binary[SnesToPc(0x0de198, self.Mapper):SnesToPc(0x0de198, self.Mapper)+3], byteorder = 'little', signed = False), self.Mapper)
			self.Secondary05FC00     = SnesToPc(int.from_bytes(self.Binary[SnesToPc(0x0de19f, self.Mapper):SnesToPc(0x0de19f, self.Mapper)+3], byteorder = 'little', signed = False), self.Mapper)
			self.Secondary05FE00     = SnesToPc(int.from_bytes(self.Binary[SnesToPc(0x05dc81, self.Mapper):SnesToPc(0x05dc81, self.Mapper)+3], byteorder = 'little', signed = False), self.Mapper)
			self.Secondary05DC86     = SnesToPc(int.from_bytes(self.Binary[SnesToPc(0x05dc86, self.Mapper):SnesToPc(0x05dc86, self.Mapper)+3], byteorder = 'little', signed = False), self.Mapper)
			self.Secondary05DC8B     = SnesToPc(int.from_bytes(self.Binary[SnesToPc(0x05dc8b, self.Mapper):SnesToPc(0x05dc8b, self.Mapper)+3], byteorder = 'little', signed = False), self.Mapper)
		else:
			self.Secondary05F800     = SnesToPc(0x05f800, self.Mapper)
			self.Secondary05FA00     = SnesToPc(0x05fa00, self.Mapper)
			self.Secondary05FC00     = SnesToPc(0x05fc00, self.Mapper)
			self.Secondary05FE00     = SnesToPc(0x05fe00, self.Mapper)
			self.Secondary05DC86     = None
			self.Secondary05DC8B     = None

		# State management for the FindFreeSpace function. Addresses are in SNES.
		self.NextFreeAddress    = 0x8a8000
		self.LastFreeAddress    = 0xbfffff
		self.FreeSpaceFragments = {}
		self.TotalWaste         = 0
		self.BytesOverflow      = 0
		self.TotalBytesWritten  = 0
		self.Layer1Dictionary   = {}
		self.Layer2Dictionary   = {}
		self.SpriteDictionary   = {}
		self.PaletteDictionary  = {}
		self.ExAnimDictionary   = {}
		self.PaletteOmitted     = 0
		self.MessageBytesCount  = 0

	def Write(self):
		with open(self.Path, 'wb') as File:
			File.write(self.Binary)

	def PrepareRegistration(self):
		# Remove VRAM patch notification
		Offset = 2179874
		if self.Binary[Offset] == 0x56 and self.Binary[Offset+3] == 0x4d and self.Binary[Offset+16] == 0x70 and self.Binary[Offset+32] == 0x28 and self.Binary[Offset+48] == 0x63:
			self.Binary[Offset:Offset+146] = bytearray(146 * [0x00])
			print('[compile.py]     Removed VRAM watermark')
		else:
			print('[compile.py]     Couldnt find VRAM watermark, perhaps it was moved?')
		
		# Clear out checksums to assist Asar in computing the correct one
		self.Binary[SnesToPc(0x00ffdc, self.Mapper)] = 0
		self.Binary[SnesToPc(0x00ffdd, self.Mapper)] = 0
		self.Binary[SnesToPc(0x00ffde, self.Mapper)] = 0xff
		self.Binary[SnesToPc(0x00ffdf, self.Mapper)] = 0xff
		self.Binary[SnesToPc(0xc07fdc, self.Mapper)] = 0
		self.Binary[SnesToPc(0xc07fdd, self.Mapper)] = 0
		self.Binary[SnesToPc(0xc07fde, self.Mapper)] = 0xff
		self.Binary[SnesToPc(0xc07fdf, self.Mapper)] = 0xff

	# Asar doesn't write the second checksum, so do it manually
	def FixChecksum(self):
		self.Binary[SnesToPc(0xc07fdc, self.Mapper)] = self.Binary[SnesToPc(0x00ffdc, self.Mapper)] 
		self.Binary[SnesToPc(0xc07fdd, self.Mapper)] = self.Binary[SnesToPc(0x00ffdd, self.Mapper)] 
		self.Binary[SnesToPc(0xc07fde, self.Mapper)] = self.Binary[SnesToPc(0x00ffde, self.Mapper)] 
		self.Binary[SnesToPc(0xc07fdf, self.Mapper)] = self.Binary[SnesToPc(0x00ffdf, self.Mapper)] 

	def Ruin(self):
		random.seed(0x27071991)
		Count = 0
		for i in range(0, len(self.Binary) - 16):
			if self.Binary[i] == b'S'[0] and self.Binary[i+1] == b'T'[0] and self.Binary[i+2] == b'A'[0] and self.Binary[i+3] == b'R'[0]:
				if ((self.Binary[i+4] ^ 0xff) == self.Binary[i+6]) and ((self.Binary[i+5] ^ 0xff) == self.Binary[i+7]):
					Count += 1
					for j in range(0, 8):
						self.Binary[i] = random.randint(0, 0xff)
						i += 1
		print('[compile.py] Destroyed {} tags!'.format(Count))

	# Change data pointers to Six Pack specific addresses. This breaks compatibility with Lunar Magic and most other tools.
	def SixPackPointers(self):
		self.Default             = False
		self.Layer1Pointers      = SnesToPc(0x069260, self.Mapper)
		self.Layer2Pointers      = SnesToPc(0x06c260, self.Mapper)
		self.SpritePointers      = SnesToPc(0x05e000, self.Mapper)
		self.SpriteBanks         = SnesToPc(0x068260, self.Mapper)
		self.StageHeader05DE00   = SnesToPc(0x0ed255, self.Mapper)
		self.StageHeader05F000   = SnesToPc(0x0fa654, self.Mapper)
		self.StageHeader05F200   = SnesToPc(0x0fb654, self.Mapper)
		self.StageHeader05F400   = SnesToPc(0x0fc654, self.Mapper)
		self.StageHeader05F600   = SnesToPc(0x0fd654, self.Mapper)
		self.StageHeader06FC00   = SnesToPc(0xc30000, self.Mapper)
		self.StageHeader06FE00   = SnesToPc(0xc31000, self.Mapper)
		self.StageHeader0EF310   = SnesToPc(0x0c8000, self.Mapper)
		self.PalettePointers     = SnesToPc(0x0780c3, self.Mapper)
		self.DemoReel            = SnesToPc(0x0df300, self.Mapper)
		self.StageExAnimPointers = SnesToPc(0x07b0c3, self.Mapper)
		self.StageHeader03FE00   = SnesToPc(0xc32000, self.Mapper)
		self.StageGraphicsBypass = SnesToPc(0xc10000, self.Mapper)
		self.Messages            = SnesToPc(0xff0000, self.Mapper)
		self.MessagePointers     = SnesToPc(0x07e0c3, self.Mapper)
		self.LevelNames          = SnesToPc(0xc0c700, self.Mapper)
		self.ContestNumbers      = SnesToPc(0x0cd500, self.Mapper)
		self.AuthorNames         = SnesToPc(0x0c9000, self.Mapper)

		# Clear demo reel
		self.Binary[self.DemoReel:self.DemoReel+1536] = [0] * 1536
		self.DemoReelEntries = []

	def GetCustomMarioLuigiPalette(self, CompareAgainst):
		# These levels were restored from damaged submissions which apparently break custom player palette detection
		# None of them use a custom player palette
		if ('LDC 3 [#059]' in self.Path) or ('VLDC6-077' in self.Path):
			return None

		Me = SnesToPc(0x00b2c8, self.Mapper)
		Them = SnesToPc(0x00b2c8, CompareAgainst.Mapper)
		for i in range(0, 80):
			if self.Binary[Me + i] != CompareAgainst.Binary[Them + i]:
				return self.Binary[Me:Me+80]
		return None

	def HasGlobalExAnimation(self):
		# read2(read3($0583ae)+$5B)

		if len(self.Binary) < 2097152:
			#print(self.Path, 'Size too small to have global')
			return False

		Indirect = SnesToPc(0x0583ae, self.Mapper)
		Pointer = SnesToPc(int.from_bytes(self.Binary[Indirect:Indirect+3], byteorder = 'little', signed = False), self.Mapper) + 91
		HasGlobal = not (self.Binary[Pointer] == 0 and self.Binary[Pointer+1] == 0)

		if HasGlobal:
			print(self.Path, hex(Pointer), HasGlobal)
		return HasGlobal

	# Vanilla contest allowed for applying this patch, for some reason
	def PiranhaProperty(self):
		if self.Binary[SnesToPc(0x018e8d, self.Mapper)] == 0xb9:
			return self.Binary[SnesToPc(0x018e93, self.Mapper)]
		elif self.Binary[SnesToPc(0x018e8d, self.Mapper)] == 0x20:
			return self.Binary[SnesToPc(0x01ffcc, self.Mapper)]
		elif self.Binary[SnesToPc(0x018e8d, self.Mapper)] == 0x22:
			return self.Binary[SnesToPc(0x01ffcc, self.Mapper)]
		else:
			# Most likely an invald rom image
			return 0xb

	def UsesPiranhaPatch(self):
		return self.Binary[SnesToPc(0x018e8d, self.Mapper)] != 0xb9

	# Vanilla contest allowed for applying this patch too, it seems?
	def UsesSpritesThroughPipePatch(self):
		return self.Binary[SnesToPc(0x02ac18, self.Mapper)] == 0x80

	# Rudimentary free space finder. This assumes a specific area of ROM was marked off. See asm/reserve.asm for more details.
	def FindFreeSpace(self, Length):
		for Key in self.FreeSpaceFragments:
			FragmentLength = self.FreeSpaceFragments[Key]
			if Length < FragmentLength:
				#print('Insert into slack space: {:X} (+{:X})'.format(Key, Length))
				Address = Key
				del self.FreeSpaceFragments[Key]
				if FragmentLength - Length > 0:
					self.FreeSpaceFragments[Address + Length] = FragmentLength - Length
				return SnesToPc(Address, self.Mapper)

		Address = self.NextFreeAddress
		self.NextFreeAddress += Length

		if Length > 0x8000:
			raise Exception('Request too large')
	
		if self.LastFreeAddress < 0xc00000 and (self.NextFreeAddress & 0x7fff) < (Address & 0x7fff):
			self.FreeSpaceFragments[Address] = ((Address & 0xff0000) + 0x10000) - Address
			#print('FreeSpace Bank Jump (1) {:X} (+{:X}), waste: {:X}'.format(Address, Length, ((Address & 0xff0000) + 0x10000) - Address ))

			Address = (self.NextFreeAddress & 0xff0000) + 0x8000
			self.NextFreeAddress = Address + Length
		elif (self.NextFreeAddress & 0xffff) < (Address & 0xffff):
			self.FreeSpaceFragments[Address] = ((Address & 0xff0000) + 0x10000) - Address
			#print('FreeSpace Bank Jump (2) {:X} (+{:X}), waste: {:X}'.format(Address, Length, ((Address & 0xff0000) + 0x10000) - Address ))

			Address = (self.NextFreeAddress & 0xff0000)
			self.NextFreeAddress = Address + Length

		if self.NextFreeAddress > 0xfeffff:
			raise Exception('Ran out of space!')
		if self.NextFreeAddress > self.LastFreeAddress:
			Address = 0xc40000
			self.NextFreeAddress = Address + Length
			self.LastFreeAddress = 0xfeffff

		return SnesToPc(Address, self.Mapper)

	def InsertLevel(self, Level, Offset):
		Number = Level.GetNumber() + Offset

		Data = Level.GetLayer1()
		DataLength = len(Data)
		DataString = str(Data)
		if DataString in self.Layer1Dictionary:
			Address = self.Layer1Dictionary[DataString]
		else:
			Address = self.FindFreeSpace(DataLength)
			self.Binary[Address:Address+DataLength] = Data
			self.Layer1Dictionary[DataString] = Address
			self.TotalBytesWritten += DataLength
		self.Binary[self.Layer1Pointers + Number * 3 : self.Layer1Pointers + Number * 3 + 3] = Make24(PcToSnes(Address))

		Address = Level.GetLayer2SourcePointer()
		if Address >= 0xff0000:
			self.Binary[self.Layer2Pointers + Number * 3 : self.Layer2Pointers + Number * 3 + 3] = Make24(Address)
			self.Binary[self.StageHeader0EF310 + Number] = 0
		else:
			Data = Level.GetLayer2() if Level.Layer2IsForeground() else Level.GetLayer2Compressed()
			DataLength = len(Data)
			DataString = str(Data)
			if DataString in self.Layer2Dictionary:
				Address = self.Layer2Dictionary[DataString]
			else:
				Address = self.FindFreeSpace(DataLength)
				self.Layer2Dictionary[DataString] = Address
				self.Binary[Address:Address+DataLength] = Data
				self.TotalBytesWritten += DataLength
			self.Binary[self.Layer2Pointers + Number * 3 : self.Layer2Pointers + Number * 3 + 3] = Make24(PcToSnes(Address))
			self.Binary[self.StageHeader0EF310 + Number] = Level.Get0EF310()

		Data = Level.GetSprites()
		DataLength = len(Data)
		DataString = str(Data)
		if DataString in self.SpriteDictionary:
			Address = self.SpriteDictionary[DataString]
		else:
			Address = self.FindFreeSpace(DataLength)
			self.Binary[Address:Address+DataLength] = Data
			self.SpriteDictionary[DataString] = Address
			self.TotalBytesWritten += DataLength
		self.Binary[self.SpritePointers + Number * 2 : self.SpritePointers + Number * 2 + 2] = Make24(PcToSnes(Address))[0:2]
		self.Binary[self.SpriteBanks + Number] = Make24(PcToSnes(Address))[2]

		Data = Level.GetPalette() if self.Default else Level.GetCompressedPalette()
		DataLength = len(Data)
		DataString = str(Data)
		if DataString in self.PaletteDictionary:
			self.PaletteOmitted += 1
			Address = self.PaletteDictionary[DataString]
		else:
			Address = self.FindFreeSpace(DataLength)
			self.Binary[Address:Address+DataLength] = Data
			self.PaletteDictionary[DataString] = Address
			self.TotalBytesWritten += DataLength
		self.Binary[self.PalettePointers + Number * 3 : self.PalettePointers + Number * 3 + 3] = Make24(PcToSnes(Address))

		Data = Level.GetExAnimation()
		DataLength = len(Data)
		DataString = str(Data)
		if DataLength == 0:
			self.Binary[self.StageExAnimPointers + Number * 3 : self.StageExAnimPointers + Number * 3 + 3] = Make24(0)
		else:
			if DataString in self.ExAnimDictionary:
				Address = self.ExAnimDictionary[DataString]
			else:
				Address = self.FindFreeSpace(DataLength)
				self.Binary[Address:Address+DataLength] = Data
				self.ExAnimDictionary[DataString] = Address
				self.TotalBytesWritten += DataLength
			self.Binary[self.StageExAnimPointers + Number * 3 : self.StageExAnimPointers + Number * 3 + 3] = Make24(PcToSnes(Address))

		self.Binary[self.StageGraphicsBypass + Number * 32 : self.StageGraphicsBypass + Number * 32 + 32] = Level.GetGraphicsBypass()

		self.Binary[self.StageHeader03FE00 + Number] = Level.Get03FE00()
		self.Binary[self.StageHeader05F000 + Number] = Level.Get05F000()
		self.Binary[self.StageHeader05F200 + Number] = Level.Get05F200()
		self.Binary[self.StageHeader05F400 + Number] = Level.Get05F400()
		self.Binary[self.StageHeader05F600 + Number] = Level.Get05F600()
		self.Binary[self.StageHeader05DE00 + Number] = Level.Get05DE00()
		self.Binary[self.StageHeader06FC00 + Number] = Level.Get06FC00()
		self.Binary[self.StageHeader06FE00 + Number] = Level.Get06FE00()
		
		for Entrance in Level.GetSecondaryEntrancesAsObjects():
			Number = Entrance.GetNumber()
			self.Binary[self.Secondary05F800 + Number] = Entrance.Get05F800()
			self.Binary[self.Secondary05FA00 + Number] = Entrance.Get05FA00()
			self.Binary[self.Secondary05FC00 + Number] = Entrance.Get05FC00()
			self.Binary[self.Secondary05FE00 + Number] = Entrance.Get05FE00()
			self.Binary[self.Secondary05DC86 + Number] = Entrance.Get05DC86()
			self.Binary[self.Secondary05DC8B + Number] = Entrance.Get05DC8B()

	def InsertPaletteRows(self, Data):
		if len(Data) >= 0xd000:
			raise Exception('Palette data greater than expected')
		self.Binary[self.PaletteRows:self.PaletteRows+len(Data)] = Data

	def GetOldGraphicsBypassByListIndex(self, Index):
		if Index == 0 or Index >= 0x100:
			raise Exception('Old graphics bypass list index may not be 0 or greater than 0xff, was {:3X}'.format(Index))

		Address = SnesToPc(0x0ff200) + (Index - 1) * 4
		return self.Binary[Address : Address + 4]

	def GetLevelName(self, Number):
		# Check if rom supports custom level names
		Pc = SnesToPc(0x03bb57)
		if self.Binary[Pc] == 0xff and self.Binary[Pc+1] == 0xff and self.Binary[Pc+2] == 0xff:
			return bytearray(19 * [0x1f])

		if Number > 0x24:
			Number -= 0xDC

		if len(self.Binary) < self.LevelNames + Number * 19 + 19:
			print('\tNo name could be fetched for {}'.format(self.Path))
			return bytearray(19 * [0x1f])

		return self.Binary[self.LevelNames + Number * 19 : self.LevelNames + Number * 19 + 19]

	def SetLevelName(self, Number, Binary):
		Number = NumberToTransIndex(Number)
		self.Binary[self.LevelNames + Number * 19 : self.LevelNames + Number * 19 + 19] = Binary

	def SetLevelAuthor(self, Number, Binary):
		Number = NumberToTransIndex(Number)
		self.Binary[self.AuthorNames + Number * 23 : self.AuthorNames + Number * 23 + 23] = Binary

	def SetContestNumber(self, Number, Value):
		Number = NumberToTransIndex(Number)
		self.Binary[self.ContestNumbers + Number] = Value

	def GetMessageForLevel(self, Number, Which, Stage):
		if Which != 0 and Which != 1:
			raise Exception('Levels only have two messages, but {} requested!'.format(Which))
		
		if Number > 0x24:
			Number -= 0xDC
		
		Length = 0
		Offset = self.Messages + int.from_bytes(self.Binary[self.MessagePointers + (Number * 2 + Which) * 2 : self.MessagePointers + (Number * 2 + Which) * 2 + 2], byteorder = 'little', signed = False) 

		if Offset > len(self.Binary):
			#print('\tMessage content pointer invalid: {} {:3X}'.format(Stage.Name, Stage.Translevel.OriginalNumber))
			return bytearray([0xFE])

		while Length < 144 and self.Binary[Offset+Length] != 0xFE:
			Length += 1
		
		Message = self.Binary[Offset:Offset+Length]
		if len(Message) == 0:
			#print('\tNo message assigned to: {} {:3X}/{}'.format(Stage.Name, Stage.Translevel.OriginalNumber, Which))
			Message += bytearray([0xFE])
		elif Message[-1] != 0xFE:
			Message += bytearray([0xFE])
		return Message

	def SetMessageForLevel(self, Number, Which, Binary):
		if Which != 0 and Which != 1:
			raise Exception('Levels only have two messages, but {} requested!'.format(Which))

		Number = NumberToTransIndex(Number)
		
		Offset = self.Messages + self.MessageBytesCount

		# Preserve secondary rom header
		#if self.MessageBytesCount < 0x7fc0 and Offset + len(Binary) >= SnesToPc(0xc07fc0, self.Mapper):
		#	self.MessageBytesCount = 0x8000
		#	Offset = self.Messages + self.MessageBytesCount

		self.MessageBytesCount += len(Binary)
		self.Binary[Offset : Offset + len(Binary)] = Binary
		self.Binary[self.MessagePointers + (Number * 2 + Which) * 2 : self.MessagePointers + (Number * 2 + Which) * 2 + 2] = struct.pack("<H", Offset - self.Messages)

	def SetDefaultMessages(self):
		Number = 0x00
		Message = "                                                      Undefined message! "
		Message = Ascii2Smw(Message, len(Message))
		Message[-1] = 0xFE

		Offset = self.Messages
		self.MessageBytesCount += len(Message)
		self.Binary[Offset : Offset + len(Message)] = Message

		while Number < 0x60:
			for Which in [0, 1]:
				self.Binary[self.MessagePointers + (Number * 2 + Which) * 2 : self.MessagePointers + (Number * 2 + Which) * 2 + 2] = struct.pack("<H", Offset - self.Messages)
			Number += 1

	def AddToDemoReel(self, Level, Offset):
		Number = Level.GetNumber() + Offset
		self.DemoReelEntries.append(Number)

	def FinalizeDemoReel(self):
		random.seed(0x5241474559)
		random.shuffle(self.DemoReelEntries)

		for i in range(0, len(self.DemoReelEntries)):
			self.Binary[self.DemoReel + i] = (self.Binary[self.DemoReel + i] & 0xf0) | ((self.DemoReelEntries[i] >> 8) & 0xff)
			self.Binary[self.DemoReel + i + 768] = self.DemoReelEntries[i] & 0xff
		
		print('[compile.py] Demo reel contains {} levels! Last index would be {:3X}'.format(len(self.DemoReelEntries), len(self.DemoReelEntries) - 1))

	def SetStageExits(self, Stage, Offset):
		Goals = Stage.GetGoals()
		Number = NumberToTransIndex(Stage.Translevel.GetNumber() + Offset)
		Data = (0x80 if Goals[0] else 0) | (0x40 if Goals[1] else 0)
		self.Binary[self.DemoReel + Number] = (self.Binary[self.DemoReel + Number] & 0x3f) | Data
		Stage.Verbose += '\tGoals: {},{} written to TransLevelNumber {:3X}\n'.format(Goals[0], Goals[1], Number)
		return sum(Goals)
	
	def SetPiranhaFlags(self, Stage, Offset):
		Data = 0x20 if Stage.SuperMarioWorld.UsesPiranhaPatch() else 0
		Number = NumberToTransIndex(Stage.Translevel.GetNumber() + Offset)
		self.Binary[self.DemoReel + Number] = (self.Binary[self.DemoReel + Number] & 0xdf) | Data
		Stage.Verbose += '\tLevel uses piranha patch? {:X} for TransLevelNumber {:3X} \n'.format(Data, Number)

	def SetSpritesPipesFlags(self, Stage, Offset):
		Data = 0x10 if Stage.SuperMarioWorld.UsesSpritesThroughPipePatch() else 0
		Number = NumberToTransIndex(Stage.Translevel.GetNumber() + Offset)
		self.Binary[self.DemoReel + Number] = (self.Binary[self.DemoReel + Number] & 0xef) | Data
		Stage.Verbose += '\tLevel uses sprites through pipes patch? {:X} for TransLevelNumber {:3X} \n'.format(Data, Number)

	def InsertGfx33User(self, Stage, Offset):
		if self.Gfx33Index >= 32:
			raise Exception('Too many GFX33 remaps')
		if Stage.RemapGfx33 != None:
			self.Binary[self.Gfx33Users + self.Gfx33Index : self.Gfx33Users + self.Gfx33Index + 2] = struct.pack("<H", Stage.Translevel.GetNumber() + Offset) 
			self.Binary[self.Gfx33Identifiers + self.Gfx33Index : self.Gfx33Identifiers + self.Gfx33Index + 2] = struct.pack("<H", Stage.RemapGfx33)
			self.Gfx33Index += 2

	def InsertCustomMarioLuigiPalette(self, Stage, Offset):
		Number = NumberToTransIndex(Stage.Translevel.GetNumber() + Offset)
		if Stage.MarioLuigiPalette is not None:
			self.Binary[self.CustomMLPalette:self.CustomMLPalette+80] = Stage.MarioLuigiPalette
			self.CustomMLPalette += 80
			self.CustomMLIndex += 1
			Stage.Verbose += '\Stage uses custom mario/luigi palette, with index {:X}\n'.format(self.CustomMLIndex - 1)
			return self.CustomMLIndex - 1
		else:
			return 0

def NumberToTransIndex(Number):
	Old = Number
	Trans = Number & 0x1ff
	if Trans > 0x24:
		Trans -= 0xDC
	while Number >= 0x200:
		Number -= 0x200
		Trans += 0x60
	return Trans

def Ascii2Smw(Value, MaxLength):
	Converted = bytearray([0x1F] * MaxLength)

	for i in range(min(MaxLength, len(Value))):
		Ascii = ord(Value[i])
		if Ascii >= 0x41 and Ascii <= 0x5A:		# Capital
			Converted[i] = Ascii - 0x41
		elif Ascii >= 0x61 and Ascii <= 0x7A:	# Lowercase
			Converted[i] = Ascii - 0x21
		elif Ascii == 0x30:						# 0
			Converted[i] = 0x6B
		elif Ascii >= 0x31 and Ascii <= 0x37:	# 1-7
			Converted[i] = Ascii + 0x33
		elif Ascii == 0x38:						# 8
			Converted[i] = 0x7B
		elif Ascii == 0x39:						# 9
			Converted[i] = 0x7C
		elif Ascii == 0x20:						# Space
			Converted[i] = 0x1F
		elif Ascii == 0x21:						# !
			Converted[i] = 0x1A
		elif Ascii == 0x26 or Ascii == 0x2B:	# &
			Converted[i] = 0x5F
		elif Ascii == 0x27:						# '
			Converted[i] = 0x5D
		elif Ascii == 0x2C:						# ,
			Converted[i] = 0x1D
		elif Ascii == 0x2D:						# -
			Converted[i] = 0x1C
		elif Ascii == 0x2E:						# .
			Converted[i] = 0x1B
		elif Ascii == 0x3F:						# ?
			Converted[i] = 0x1E
		elif Ascii == 0x5F:						# _
			Converted[i] = 0x6C
		elif Ascii == 0x28:						# (
			Converted[i] = 0x5B
		elif Ascii == 0x29:						# )
			Converted[i] = 0x5C
		else:									# Unhandled character
			Converted[i] = 0x1F
			raise Exception('Unhandled character in Ascii2Smw')

	return Converted