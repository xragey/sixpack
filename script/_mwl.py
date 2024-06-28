###############################################################################
#
# SIX PACK by Ragey <i@ragey.net>
# _mwl.py
#
###############################################################################

import struct
from _rle import *

###############################################################################

class MarioWorldLevel():
	def __init__(self, Path, SourceRom):
		with open(Path, 'rb') as File:
			self.Binary = bytearray(File.read())
		
		if self.Binary[2] != 0x32 or self.Binary[3] != 0x03:
			print('Warning: This .mwl file is not made with Lunar Magic 3.32!')
		
		self.Header = self.Binary[0:64]

		OffsetsOffset = int.from_bytes(self.Binary[4:8], byteorder = 'little', signed = False)
		OffsetsSize = int.from_bytes(self.Binary[8:12], byteorder = 'little', signed = False)
		self.Offsets = self.Binary[OffsetsOffset:OffsetsOffset+OffsetsSize]

		LevelInfoOffset = int.from_bytes(self.Offsets[0:4], byteorder = 'little', signed = False)
		LevelInfoSize = int.from_bytes(self.Offsets[4:8], byteorder = 'little', signed = False)
		self.LevelInfo = self.Binary[LevelInfoOffset:LevelInfoOffset+LevelInfoSize]

		Layer1Offset = int.from_bytes(self.Offsets[8:12], byteorder = 'little', signed = False)
		Layer1Size = int.from_bytes(self.Offsets[12:16], byteorder = 'little', signed = False)
		self.Layer1 = self.Binary[Layer1Offset:Layer1Offset+Layer1Size]

		Layer2Offset = int.from_bytes(self.Offsets[16:20], byteorder = 'little', signed = False)
		self.Layer2Size = int.from_bytes(self.Offsets[20:24], byteorder = 'little', signed = False)
		self.Layer2 = self.Binary[Layer2Offset:Layer2Offset+self.Layer2Size]

		SpritesOffset = int.from_bytes(self.Offsets[24:28], byteorder = 'little', signed = False)
		SpritesSize = int.from_bytes(self.Offsets[28:32], byteorder = 'little', signed = False)
		self.Sprites = self.Binary[SpritesOffset:SpritesOffset+SpritesSize]

		PaletteOffset = int.from_bytes(self.Offsets[32:36], byteorder = 'little', signed = False)
		PaletteSize = int.from_bytes(self.Offsets[36:40], byteorder = 'little', signed = False)
		self.Palette = self.Binary[PaletteOffset:PaletteOffset+PaletteSize]
		self.CompressedPalette = self.Binary[PaletteOffset:PaletteOffset+PaletteSize]

		SecondaryEntrancesOffset = int.from_bytes(self.Offsets[40:44], byteorder = 'little', signed = False)
		SecondaryEntrancesSize = int.from_bytes(self.Offsets[44:48], byteorder = 'little', signed = False)
		self.SecondaryEntrances = self.Binary[SecondaryEntrancesOffset:SecondaryEntrancesOffset+SecondaryEntrancesSize]

		ExAnimationOffset = int.from_bytes(self.Offsets[48:52], byteorder = 'little', signed = False)
		ExAnimationSize = int.from_bytes(self.Offsets[52:56], byteorder = 'little', signed = False)
		self.ExAnimation = self.Binary[ExAnimationOffset:ExAnimationOffset+ExAnimationSize]

		GraphicsBypassOffset = int.from_bytes(self.Offsets[56:60], byteorder = 'little', signed = False)
		GraphicsBypassSize = int.from_bytes(self.Offsets[60:64], byteorder = 'little', signed = False)
		self.GraphicsBypass = self.Binary[GraphicsBypassOffset:GraphicsBypassOffset+GraphicsBypassSize]

		self.Path = Path
		self.Accessible = False
		self.InDemoReel = False
		self.SourceRom = SourceRom
		self.OriginalNumber = self.GetNumber()

	def Write(self, OutPath):
		with open(OutPath, 'wb') as File:
			File.write(self.Header)

			Offset = len(self.Header) + len(self.Offsets)
			File.write(struct.pack("<I", Offset))
			File.write(struct.pack("<I", len(self.LevelInfo)))

			Offset += len(self.LevelInfo)
			File.write(struct.pack("<I", Offset))
			File.write(struct.pack("<I", len(self.Layer1)))

			Offset += len(self.Layer1)
			File.write(struct.pack("<I", Offset))
			File.write(struct.pack("<I", len(self.Layer2)))

			Offset += len(self.Layer2)
			File.write(struct.pack("<I", Offset))
			File.write(struct.pack("<I", len(self.Sprites)))

			Offset += len(self.Sprites)
			File.write(struct.pack("<I", Offset))
			File.write(struct.pack("<I", len(self.Palette)))

			Offset += len(self.Palette)
			File.write(struct.pack("<I", Offset))
			File.write(struct.pack("<I", len(self.SecondaryEntrances)))

			Offset += len(self.SecondaryEntrances)
			File.write(struct.pack("<I", Offset))
			File.write(struct.pack("<I", len(self.ExAnimation)))

			Offset += len(self.ExAnimation)
			File.write(struct.pack("<I", Offset))
			File.write(struct.pack("<I", len(self.GraphicsBypass)))

			File.write(self.LevelInfo)
			File.write(self.Layer1)
			File.write(self.Layer2)
			File.write(self.Sprites)
			File.write(self.Palette)
			File.write(self.SecondaryEntrances)
			File.write(self.ExAnimation)
			File.write(self.GraphicsBypass)

	def GetNumber(self):
		return int.from_bytes(self.LevelInfo[0:2], byteorder = 'little', signed = False)

	def SetNumber(self, Number):
		self.LevelInfo[0:2] = struct.pack("<H", Number)
	
	def Get03FE00(self):
		return self.ExAnimation[0]

	def Get05F000(self):
		return self.LevelInfo[2]

	def Get05F200(self):
		return self.LevelInfo[3]
	
	def Get05F400(self):
		return self.LevelInfo[4]
	
	def Get05F600(self):
		return self.LevelInfo[5]

	def Get05DE00(self):
		return self.LevelInfo[6]

	def GetMidway0(self):
		return self.LevelInfo[9]

	def GetMidway1(self):
		return self.LevelInfo[10]

	def GetMidway2(self):
		return self.LevelInfo[11]

	def GetMidway3(self):
		return self.LevelInfo[12]

	def Get06FC00(self):
		return self.LevelInfo[14]
	
	def Get06FE00(self):
		return self.LevelInfo[15]
	
	def GetExLevel(self):
		return self.LevelInfo[16]

	def Get0EF310(self):
		return self.Layer2[0]

	def IsVertical(self):
		Mode = self.GetLayer1()[1] & 0x1f
		return Mode == 0x3 or Mode == 0x4 or Mode == 0x7 or Mode == 0x8 or Mode == 0xa or Mode == 0xd

	def GetLayer1(self):
		return self.Layer1[8:]
	
	def GetLayer2(self):
		return self.Layer2[8:]

	def GetTileset(self):
		return self.Layer1[12] & 0x0F
	
	def IsBossLevel(self):
		Mode = self.GetLayer1()[1] & 0x1f
		return Mode == 0x9 or Mode == 0xb or Mode == 0x10

	def GetLayer2Compressed(self):
		if self.Layer2IsForeground():
			raise Exception('Cannot compress layer 2 foreground structure')
		return CompressBackgroundImage(self.GetLayer2())

	def GetLayer2SourcePointer(self):
		return int.from_bytes(self.Layer2[4:7], byteorder = 'little', signed = False)

	def Layer2IsForeground(self):
		return not (self.Layer2[0] & 0x04)

	def GetForegroundDirectMap16(self, Collection):
		for Layer in [1, 2]:
			if Layer == 1:
				Sequence = ParseLayerIntoObjects(self.GetLayer1())
			elif Layer == 2 and self.Layer2IsForeground():
				Sequence = ParseLayerIntoObjects(self.GetLayer2())
			else:
				return

			for Object in Sequence:
				Number = Object.GetNumber()

				if Number == 0x22 or Number == 0x23:
					Map16 = Object.Binary[3] | ((Object.Binary[1] & 0x10) << 4)
					Collection[Map16] = (0, 0, self.GetTileset())
				
				elif Number == 0x27 or Number == 0x29:
					Map16 = Object.Binary[4] | ((Object.Binary[3] & 0x3F) << 8)

					if Number == 0x29:
						Map16 += 0x4000
					
					if Object.Binary[3] & 0xC0 == 0x00:		# Single tile
						if not Map16 in Collection:
							Collection[Map16] = (0, 0, self.GetTileset())
					
					elif Object.Binary[3] & 0xC0 == 0x40:	# Multiple tiles unstretched
						Width = Object.Binary[2] & 0x0F
						Height = (Object.Binary[2] & 0xF0) >> 4
						if not Map16 in Collection:
							Collection[Map16] = (Width, Height, self.GetTileset())
						else:
							Collection[Map16] = (max(Width, Collection[Map16][0]), max(Height, Collection[Map16][1]), self.GetTileset())
					
					else:
						Width = Object.Binary[5] & 0x0F
						Height = (Object.Binary[5] & 0xF0) >> 4
						if not Map16 in Collection:
							Collection[Map16] = (Width, Height, self.GetTileset())
						else:
							Collection[Map16] = (max(Width, Collection[Map16][0]), max(Height, Collection[Map16][1]), self.GetTileset())

	def RemapForegroundDirectMap16(self, Map):
		for Layer in [1, 2]:
			if Layer == 1:
				Sequence = ParseLayerIntoObjects(self.GetLayer1())
			elif Layer == 2 and self.Layer2IsForeground():
				Sequence = ParseLayerIntoObjects(self.GetLayer2())
			else:
				return
			
			for Object in Sequence:
				Number = Object.GetNumber()
				if Number == 0x22 or Number == 0x23 or Number == 0x27 or Number == 0x29:
					Tile, XStretch, YStretch = Object.GetDirectMap16()
					if Tile in Map:
						Object.SetDirectMap16(Tile, Map[Tile])
			
			if Layer == 1:
				self.Layer1 = self.Layer1[:13] + EncodeObjectsIntoBinary(Sequence)
			elif Layer == 2:
				self.Layer2 = self.Layer2[:13] + EncodeObjectsIntoBinary(Sequence)

	def ApplyMap16RemapObject(self, RemapDictionary):
		Count = len(RemapDictionary)

		if Count < 1:
			return
		
		if self.Layer2IsForeground():
			Objects = ParseLayerIntoObjects(self.GetLayer2())
		else:
			Objects = ParseLayerIntoObjects(self.GetLayer1())

		Count -= 1
		Binary = bytearray([((Count & 0x1ff) >> 4), (Count & 0xf), 0x04, 0xff])
		
		for Key in RemapDictionary:
			if Key < 0x200:
				Binary += bytearray([Key & 0xff, ((Key >> 1) & 0x80) | ((RemapDictionary[Key] >> 8) & 0x7f), RemapDictionary[Key] & 0xff])

		Objects.append(SMWObject(Binary))

		if self.Layer2IsForeground():
			self.Layer2 = self.Layer2[:13] + EncodeObjectsIntoBinary(Objects)
		else:
			self.Layer1 = self.Layer1[:13] + EncodeObjectsIntoBinary(Objects)

	def GetBackgroundTilemap(self):
		if self.Layer2IsForeground():
			return []

		Tiles = []

		i = 8	# .mwl header
		while i < len(self.Layer2):
			Tiles.append(int.from_bytes(self.Layer2[i:i+2], byteorder = 'little', signed = False))
			i += 2
		
		Base = 0x8000 | ((self.Layer2[0] & 0xf0) << 8)
		return [x|Base for x in [*{*Tiles}]]

	def RemapBackgroundTilemap(self, Mapping, Using0900):
		if self.Layer2IsForeground():
			raise Exception('Attempting BG logic on tiled layer 2')
		
		Layer = self.GetLayer2()
		BackupLayer = self.Layer2
		ValidTile = None
		Base = 0x8000 | ((self.Layer2[0] & 0xf0) << 8)

		i = 0
		while i < self.Layer2Size - 8:
			Tile = (int.from_bytes(Layer[i:i+2], byteorder = 'little', signed = False) | Base)

			if Tile in Mapping:
				ValidTile = Tile
				Layer[i:i+2] = struct.pack("<H", Mapping[Tile] - (0x9000 if Using0900 else 0x8000))
				# Mark the background as not-from-vanilla if at least one tile in native map16 was changed
				if (Tile & 0xfff) < 0x200:
					self.Layer2[6] = 0

			i += 2

		if self.Layer2[6] == 0xff:
			self.Layer2 = BackupLayer
			return

		self.Layer2 = self.Layer2[:8] + Layer

		if ValidTile != None and Mapping[ValidTile] >= 0x9000:
			self.Layer2[0] = (self.Layer2[0] & 0xf) | 0x16
		elif ValidTile != None:
			self.Layer2[0] = (self.Layer2[0] & 0xf) | 0x06

	def HasYoshiWings(self):
		ByteDistanceCheck = 0 if self.IsVertical() else 1

		for Object in ParseLayerIntoObjects(self.GetLayer1()):
			Number = Object.GetNumber()
			if Number == 0x00 and Object.Binary[2] == 0x35 and (Object.Binary[ByteDistanceCheck] % 4) == 1:
				return True
			Tile, XStretch, YStretch = Object.GetDirectMap16()
			if Tile == 0x125 and (Object.Binary[ByteDistanceCheck] % 4) == 1:
				return True
		
		if self.Layer2IsForeground():
			for Object in ParseLayerIntoObjects(self.GetLayer2()):
				Number = Object.GetNumber()
				if Number == 0x00 and Object.Binary[2] == 0x35 and (Object.Binary[ByteDistanceCheck] % 4) == 1:
					return True
				Tile, XStretch, YStretch = Object.GetDirectMap16()
				if Tile == 0x125 and (Object.Binary[ByteDistanceCheck] % 4) == 1:
					return True
		
		return False

	def AddYoshiWingsExitObject(self, TargetLevelNumber):
		Objects = ParseLayerIntoObjects(self.GetLayer1())
		Objects.insert(0, SMWObject(bytearray([(TargetLevelNumber >> 4) & 0x1f, TargetLevelNumber & 0xf, 0x05])))
		self.Layer1 = self.Layer1[:13] + EncodeObjectsIntoBinary(Objects)
	
	def AddMarioLuigiPaletteObject(self, Identifier):
		Objects = ParseLayerIntoObjects(self.GetLayer1())
		Objects.insert(0, SMWObject(bytearray([(Identifier) & 0x1f, (Identifier >> 4) & 0x06, 0x06])))
		self.Layer1 = self.Layer1[:13] + EncodeObjectsIntoBinary(Objects)
	
	def AddSecondaryEntrance(self, Identifier, SourceRom):
		# Ignore if identifier already exists
		for Entrance in self.GetSecondaryEntrancesAsObjects():
			if Entrance.GetNumber() == Identifier:
				return
		
		Secondary05F800 = SourceRom.Binary[SourceRom.Secondary05F800 + Identifier]
		Secondary05FA00 = SourceRom.Binary[SourceRom.Secondary05FA00 + Identifier]
		Secondary05FC00 = SourceRom.Binary[SourceRom.Secondary05FC00 + Identifier]
		Secondary05FE00 = SourceRom.Binary[SourceRom.Secondary05FE00 + Identifier]
		Secondary05DC86 = SourceRom.Binary[SourceRom.Secondary05DC86 + Identifier] if SourceRom.Secondary05DC86 else 0
		Secondary05DC8B = SourceRom.Binary[SourceRom.Secondary05DC8B + Identifier] if SourceRom.Secondary05DC8B else 0
		
		Data = bytearray([Identifier & 0xff, (Identifier >> 8) & 0xff, Secondary05FA00, Secondary05FC00, Secondary05FE00, Secondary05DC86, Secondary05DC8B, 0])
		self.SecondaryEntrances += Data

	def GetSecondaryEntrancesAsNumbers(self):
		Numbers = []
		i = 0
		while i < len(self.SecondaryEntrances[8:]):
			Numbers.append(self.SecondaryEntrances[8+i] | (self.SecondaryEntrances[9+i] << 8))
			i += 8
		return Numbers

	def GetSecondaryEntrancesAsObjects(self):
		i = 8
		Entrances = []
		while i < len(self.SecondaryEntrances):
			Entrances.append(SecondaryEntrance(self.GetNumber(), self.SecondaryEntrances[i:i+8]))
			i += 8
		return Entrances

	def RemoveSecondaryEntranceByNumber(self, Number):
		i = 0
		while i < len(self.SecondaryEntrances[8:]):
			if self.SecondaryEntrances[8+i] | (self.SecondaryEntrances[9+i] << 8) == Number:
				del self.SecondaryEntrances[8+i:8+i+8]
				return True
			i += 8
		return False

	def RemapSecondaryEntrances(self, SecondaryEntranceNumber, RemapDictionary):
		i = 0
		while i < len(self.SecondaryEntrances[8:]):
			Number = (self.SecondaryEntrances[8+i] | (self.SecondaryEntrances[9+i] << 8))
			self.SecondaryEntrances[8+i] = SecondaryEntranceNumber & 0xff
			self.SecondaryEntrances[9+i] = (SecondaryEntranceNumber) >> 8 & 0x7f
			if Number not in RemapDictionary:
				RemapDictionary[Number] = SecondaryEntranceNumber
				SecondaryEntranceNumber += 1
			i += 8
		return SecondaryEntranceNumber

	def GetScreenExits(self):
		Exits = []
		Objects = ParseLayerIntoObjects(self.GetLayer1())
		for Object in Objects:
			IsSecondary, Number = Object.GetScreenExit()
			if Number != None:
				Exits.append((IsSecondary, Number))
		return Exits

	def RemapScreenExits(self, LevelRemapDictionary, SecondaryRemapDictionary):
		Remap = {}

		Objects = ParseLayerIntoObjects(self.GetLayer1())
		for Object in Objects:
			IsSecondary, Number = Object.GetScreenExit()
			if IsSecondary == True:
				if Number in SecondaryRemapDictionary:
					Object.SetScreenExit(SecondaryRemapDictionary[Number], self.IsVertical())
					Remap[(Number, True)] = SecondaryRemapDictionary[Number]
			elif IsSecondary == False:
				if Number in LevelRemapDictionary:
					Object.SetScreenExit(LevelRemapDictionary[Number], self.IsVertical())
					Remap[(Number, False)] = LevelRemapDictionary[Number]
		self.Layer1 = self.Layer1[:13] + EncodeObjectsIntoBinary(Objects)
		return Remap

	def RemoveMusicBypass(self):
		AmkMap = [0x29, 0xa, 0xb, 0xc, 0xd, 0xe, 0xf, 0x10, 0x11, 0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x7, 0x8, 0x12, 0x13, 0x9, 0x14, 0x1f, 0x24, 0x23, 0x20, 0x20, 0x21, 0x25, 0x22]
		DefaultMusicMapPerTileset = [0, 3, 2, 1, 7, 4, 2, 0, 2, 5, 7, 3, 0, 4, 1, 0]
		Removed = False

		Objects = ParseLayerIntoObjects(self.GetLayer1())
		for Object in Objects:
			if Object.GetNumber() == 0x26:
				if Object.Binary[2] > 0x1D:
					self.Layer1[10] = self.Layer1[10] & 0x8f | (DefaultMusicMapPerTileset[self.GetTileset()] << 4)
					Objects.remove(Object)
					Removed = True
				else:
					Object.Binary[2] = AmkMap[Object.Binary[2] - 1] + 1
				break

		self.Layer1 = self.Layer1[:13] + EncodeObjectsIntoBinary(Objects)
		return Removed

	def GetSprites(self):
		return self.Sprites[8:]

	def HasMessageBoxes(self):
		MessageBoxes = [False, False]

		Sprites = self.GetSprites()

		if Sprites[0] & 0x20:
			raise Exception('New sprite system is not supported!')
		
		i = 1
		while i < len(Sprites):
			if Sprites[i] == 0xFF:
				break
			if Sprites[i+2] == 0x19:
				MessageBoxes[0] = True
			if Sprites[i+2] == 0xB9:
				if (Sprites[i + (0 if self.IsVertical() else 1)] & 0x10 == 0):
					MessageBoxes[0] = True
				else:
					MessageBoxes[1] = True
			i += 3

		return MessageBoxes

	def HasCreatingSprite(self):
		Sprites = self.GetSprites()
		if Sprites[0] & 0x20:
			raise Exception('New sprite system is not supported!')
		
		i = 1
		while i < len(Sprites):
			if Sprites[i] == 0xff:
				break
			if Sprites[i+2] == 0xb1:
				if (Sprites[i + (0 if self.IsVertical() else 1)] & 0x10 == 0):
					print('{} has CREATING blocks!'.format(self.Path))
					return True
			i += 3
		return False

	# Those cheaters!
	def RemoveCustomSprites(self):
		Sprites = self.GetSprites()

		i = 1
		while i < len(Sprites):
			if Sprites[i] == 0xff:
				break
			if Sprites[i+2] > 0xdf:
				i += 3
				continue
			if ((Sprites[i] & 0xc) == 0xc) or ((Sprites[i] & 0xc) == 0x8):
				print(self.Path, 'has a custom sprite')
			i += 3

	def GetPalette(self):
		Palette = self.Palette[520:522]
		Palette.extend(self.Palette[8:520])		
		return Palette

	def SetCompressedPalette(self, Binary):
		self.CompressedPalette = self.Palette[:8] + Binary
	
	def GetCompressedPalette(self):
		return self.CompressedPalette[8:]

	def GetExAnimation(self):
		return self.ExAnimation[8:]

	def GetGraphicsBypass(self):
		return self.GraphicsBypass
	
	def IsGraphicsBypassEnabled(self):
		return self.GraphicsBypass[1] & 0x80 != 0

	def GetGraphicsBypassNumbers(self):
		if self.GraphicsBypass[1] & 0x80 == 0:
			raise Exception('This operation expects graphics bypass to be enabled')

		Numbers = []
		for i in range(0, 32, 2):
			Numbers.append(int.from_bytes(self.GraphicsBypass[i:i+2], byteorder = 'little', signed = False) & 0x0fff)
		return set(filter(lambda N: N != 0x7f, Numbers))

	def EnableGraphicsBypass(self):
		# This entry is weird in that it does appear to have ExGFX files setup but it's lacking the Lunar Magic ASM.
		# In aiming for accuracy to how the patch was delivered, we reset the bypass settings to their defaults for this
		# entry only.
		if 'VLDC3-SMWC Vanilla LDC 3 [#002]' in self.Path:
			pass
		elif self.GraphicsBypass[1] & 0x80 != 0:
			return False, 0, 0
		
		self.GraphicsBypass[1] |= 0x80

		Sequence = [ 0x7f, 0x7f, 0x7f, 0x7f ]

		# Check if old graphics bypass was used for sprites, tiles, or both.
		SpriteListIndex = 0
		BlockListIndex = 0
		for Object in ParseLayerIntoObjects(self.GetLayer1()):
			if Object.GetNumber() == 0x24:
				if self.IsVertical():
					SpriteListIndex = ((Object.Binary[1] & 0xf) << 4) | (Object.Binary[0] & 0xf)
				else:
					SpriteListIndex = ((Object.Binary[0] & 0xf) << 4) | (Object.Binary[1] & 0xf)
				BlockListIndex = Object.Binary[2]
				break

			# Old ExAnimation bypass
			if Object.GetNumber() == 0x25:
				Sequence[0] = Object.Binary[2] - 1

		# Set sprite graphics files to either the referenced old list, if any, or to the tileset default otherwise.
		if SpriteListIndex > 0:
			SpriteGFX = self.SourceRom.GetOldGraphicsBypassByListIndex(SpriteListIndex)
		else:
			SpriteGFX = [
				[0x02, 0x13, 0x01, 0x00],
				[0x03, 0x12, 0x01, 0x00],
				[0x05, 0x13, 0x01, 0x00],
				[0x04, 0x13, 0x01, 0x00],
				[0x06, 0x13, 0x01, 0x00],
				[0x09, 0x13, 0x01, 0x00],
				[0x04, 0x13, 0x01, 0x00],
				[0x11, 0x06, 0x01, 0x00],
				[0x20, 0x13, 0x01, 0x00],
				[0x0f, 0x13, 0x01, 0x00],
				[0x23, 0x13, 0x01, 0x00],
				[0x14, 0x0d, 0x01, 0x00],
				[0x0e, 0x24, 0x01, 0x00],
				[0x22, 0x0a, 0x01, 0x00],
				[0x0e, 0x13, 0x01, 0x00],
				[0x14, 0x13, 0x01, 0x00],
			]
			SpriteIndex = self.Layer1[10] & 0xf
			SpriteGFX = SpriteGFX[SpriteIndex][0], SpriteGFX[SpriteIndex][1], SpriteGFX[SpriteIndex][2],SpriteGFX[SpriteIndex][3]
		
		# Set tile graphics files to either the referenced old list, if any, or to the tileset default otherwise.
		if BlockListIndex > 0:
			BlockGFX = self.SourceRom.GetOldGraphicsBypassByListIndex(BlockListIndex)
		else:
			BlockGFX = [
				[0x15, 0x19, 0x17, 0x14],
				[0x18, 0x1b, 0x17, 0x14],
				[0x16, 0x1b, 0x17, 0x14],
				[0x1a, 0x0c, 0x17, 0x14],
				[0x08, 0x1b, 0x17, 0x14],
				[0x07, 0x0c, 0x17, 0x14],
				[0x16, 0x0c, 0x17, 0x14],
				[0x15, 0x1b, 0x17, 0x14],
				[0x16, 0x19, 0x17, 0x14],
				[0x1a, 0x0d, 0x17, 0x14],
				[0x08, 0x1b, 0x17, 0x14],
				[0x18, 0x1b, 0x17, 0x14],
				[0x1f, 0x19, 0x17, 0x14],
				[0x07, 0x0d, 0x17, 0x14],
				[0x1a, 0x19, 0x17, 0x14],
			]
			BlockIndex = self.Layer1[12] & 0xf
			BlockGFX = BlockGFX[BlockIndex][0], BlockGFX[BlockIndex][1], BlockGFX[BlockIndex][2],BlockGFX[BlockIndex][3],

		Sequence.extend(BlockGFX)
		Sequence.extend(SpriteGFX)

		for i in range(0, 24, 2):
			self.GraphicsBypass[i:i+2] = struct.pack("<H", (int.from_bytes(self.GraphicsBypass[i:i+2], byteorder = 'little', signed = False) & 0xf000) | Sequence[i // 2])	

		return True, SpriteListIndex, BlockListIndex

	def RemapGraphicsBypass(self, ExGFXNumber, GraphicsToChangeList, RemapDictionary):
		if self.GraphicsBypass[1] & 0x80 == 0:
			raise Exception('This operation expects graphics bypass to be enabled')

		for i in range(0, 32, 2):
			Value = int.from_bytes(self.GraphicsBypass[i:i+2], byteorder = 'little', signed = False)
			
			# Check if a hardcoded exception needs to be applied
			if Value == 0x08:
				if 'VLDC4-SMWC Vanilla LDC 4 [#65]' in self.Path:
					self.GraphicsBypass[i:i+2] = struct.pack("<H", 0x86 | (Value & 0xf000))			
			if Value == 0x1E:
				if 'VLDC4-SMWC Vanilla LDC 4 [#65]' in self.Path or 'VLDC2-018' in self.Path:
					self.GraphicsBypass[i:i+2] = struct.pack("<H", 0x85 | (Value & 0xf000))
				else:
					pass
					#print('{} uses 0x1E'.format(self.Path))
			# Otherwise apply standard remap
			else:
				Graphic = Value & 0xfff
				if Graphic in GraphicsToChangeList:
					if Graphic not in RemapDictionary:
						RemapDictionary[Graphic] = ExGFXNumber
						ExGFXNumber += 1
					self.GraphicsBypass[i:i+2] = struct.pack("<H", RemapDictionary[Graphic] | (Value & 0xf000))

		return ExGFXNumber

	def RemoveGraphicsBypass(self, ExGFXNumber):
		if self.GraphicsBypass[1] & 0x80 == 0:
			raise Exception('This operation expects graphics bypass to be enabled')
		
		for i in range(0, 32, 2):
			Value = int.from_bytes(self.GraphicsBypass[i:i+2], byteorder = 'little', signed = False)
			Graphic = Value & 0xfff
			if Graphic == ExGFXNumber:
				self.GraphicsBypass[i:i+2] = struct.pack("<H", 0x7f | (Value & 0xf000))

	def GetGoals(self):
		Goals = [False, False]
		Sprites = self.GetSprites()

		i = 1
		while i < len(Sprites):
			if Sprites[i] == 0xFF:
				break
			if Sprites[i+2] == 0x7B: # Goal tape
				if Sprites[i] & 0x0c == 0:
					Goals[0] = True
				else:
					Goals[1] = True
			elif Sprites[i+2] == 0x4A: # Orb
				Goals[0] = True
			elif Sprites[i+2] == 0x0E: # Keyhole
				Goals[1] = True
			elif Sprites[i+2] == 0xC5: # Big Boo Boss
				Goals[0] = True
			elif Sprites[i+2] == 0x29: # Koopa Kid
				Goals[0] = True
			elif Sprites[i+2] == 0xA0: # Bowsah
				Goals[0] = True
			elif Sprites[i+2] == 0xA9: # Reznor
				Goals[0] = True
			i += 3
		
		if self.HasYoshiWings():
			Goals[0] = True

		for Layer in [1, 2]:
			if Layer == 1:
				Sequence = ParseLayerIntoObjects(self.GetLayer1())
			elif Layer == 2 and self.Layer2IsForeground():
				Sequence = ParseLayerIntoObjects(self.GetLayer2())
			else:
				continue
		
			for Object in Sequence:
				Number = Object.GetNumber()
				if Number == 0x00 and (Object.Binary[2] == 0x8a or Object.Binary[2] == 0x8b or Object.Binary[2] == 0x8c or Object.Binary[2] == 0x8d):
					Goals[0] = True
				Tile, X, Y = Object.GetDirectMap16()
				if Tile == 0xec or Tile == 0xed or Tile == 0xf0 or Tile == 0xf1 or Tile == 0xf4 or Tile == 0xf5 or Tile == 0xf8 or Tile == 0xf9:
					Goals[0] = True

		return Goals

	def NormalizeTime(self):
		Objects = ParseLayerIntoObjects(self.GetLayer1())
		for Object in Objects:
			if Object.GetNumber() == 0x28:
				for i in [0, 1, 2]:
					if (Object.Binary[i] & 0xf) > 0x9:
						Object.Binary[i] = (Object.Binary[i] & 0xf0) | 0x9
		self.Layer1 = self.Layer1[:13] + EncodeObjectsIntoBinary(Objects)

class SecondaryEntrance:
	def __init__(self, LevelNumber, Binary):
		self.Binary = Binary
		self.LevelNumber = LevelNumber
	
	def GetNumber(self):
		return self.Binary[0] | (self.Binary[1] << 8)
	
	def Get05F800(self):
		return self.LevelNumber & 0xff
	
	def Get05FA00(self): 
		return self.Binary[2]
	
	def Get05FC00(self):
		return self.Binary[3]
	
	def Get05FE00(self):
		return (self.Binary[4] & 0xf7) | ((self.LevelNumber >> 5) & 0x08)
	
	def Get05DC86(self):
		return self.Binary[5]
	
	def Get05DC8B(self):
		return self.Binary[6]

class SMWObject:
	def __init__(self, Binary):
		self.Binary = Binary

		# First byte being 0xFF indicates the end of data.
		if Binary[0] == 0xff:
			self.Binary = Binary[:1]
			return
		
		# Get the bytes that belong to this object and cut off the remainder.
		Number = self.GetNumber()

		if Number == 0x00:
			if Binary[2] == 0x00:
				self.Binary = Binary[:4]
			elif Binary[2] == 0x02:
				self.Binary = Binary[:5]
			elif Binary[2] == 0x04:			# Custom Six Pack object!
				self.Binary = Binary
			else:
				self.Binary = Binary[:3]
		elif Number == 0x22 or Number == 0x23:
			self.Binary = Binary[:4]
		elif Number == 0x27 or Number == 0x29:
			if Binary[3] & 0x80 == 0:
				self.Binary = Binary[:5]
			elif Binary[3] & 0xC0 == 0x80:
				self.Binary = Binary[:6]
			elif Binary[2] & 0x80 == 0:
				self.Binary = Binary[:7]
			elif Binary[2] & 0x80 == 0x80:
				self.Binary = Binary[:8]
			else:
				raise Exception('Unexpected data for object 0x27/0x29!')
		elif Number == 0x2D:
			self.Binary = Binary[:5]
		else:
			self.Binary = Binary[:3]

	def GetNumber(self):
		return ((self.Binary[1] & 0xF0) >> 4) | ((self.Binary[0] & 0x60) >> 1)

	def GetSize(self):
		return len(self.Binary)
	
	def GetExtendedNumber(self):
		return self.Binary[2] if self.GetNumber() == 0 else None
	
	# Multiple returns TileID, XStretch, YStretch
	def GetDirectMap16(self):
		Number = self.GetNumber()

		if Number == 0x22 or Number == 0x23:
			Map16 = self.Binary[3] | ((self.Binary[1] & 0x10) << 4)
			return Map16, 0, 0
		elif Number == 0x27 or Number == 0x29:
			Map16 = self.Binary[4] | ((self.Binary[3] & 0x3F) << 8) + (0 if Number == 0x27 else 0x4000)
			if (self.Binary[3] & 0xC0) == 0:
				return Map16, 0, 0
			elif (self.Binary[3] & 0xC0) == 0x40:
				return Map16, self.Binary[2] & 0x0F, (self.Binary[2] & 0xF0) >> 4
			else:
				return Map16, self.Binary[5] & 0x0F, (self.Binary[5] & 0xF0) >> 4
		return None, None, None
	
	def SetDirectMap16(self, SourceTile, ChangeIntoTile):
		Number = self.GetNumber()

		if Number == 0x22 or Number == 0x23:
			Map16 = self.Binary[3] | ((self.Binary[1] & 0x10) << 4)
			if Map16 == SourceTile:
				self.Binary = bytearray([
					self.Binary[0],
					(self.Binary[1] & 0x0f) | (0x70 if ChangeIntoTile < 0x4000 else 0x90),
					self.Binary[2],
					(ChangeIntoTile >> 8) & 0x3f,
					ChangeIntoTile & 0xff
				])
		elif Number == 0x27 or Number == 0x29:
			Map16 = self.Binary[4] | ((self.Binary[3] & 0x3f) << 8)
			if Map16 == SourceTile:
				self.Binary[4] = ChangeIntoTile & 0xff
				self.Binary[3] = (self.Binary[3] & 0xc0) | ((ChangeIntoTile >> 8) & 0x3f)
				self.Binary[1] = (self.Binary[1] & 0x0f) | (0x70 if ChangeIntoTile < 0x4000 else 0x90)
		else:
			raise Exception('Attempting to change Map16 of a non-DirectMap16 object!')

	# Multiple returns IsSecondaryExit, Number
	def GetScreenExit(self):
		if self.GetNumber() == 0 and self.GetExtendedNumber() == 0:
			return self.Binary[1] & 0x02 == 0x02, self.Binary[3] | ((self.Binary[1] & 0x01) << 8)
		elif self.GetNumber() == 0 and self.GetExtendedNumber() == 2:
			raise Exception('New-style secondary exits are not supported!')
		else:
			return None, None

	# Assumes the source secondaries are always first generation, which is true for my dataset.
	# Level numbers above 0x1FF are allowed, but a normal SMW hack would not support that.
	def SetScreenExit(self, Number, IsVertical):		
		if Number < 0x200:
			self.Binary[1] = (self.Binary[1] & 0x0e) | ((Number >> 8) & 0x01)
			self.Binary[3] = Number & 0xff
		else:
			# The format on speedrun wiki is only correct for horizontal stages; for vertical stages it is
			# instead the screen on bytes 0 and 1 in format 000p---- 0000pppp instead of 000ppppp 0000----
			self.Binary.append((self.Binary[1] & 0x8) | 0x6 | ((Number & 0x100) >> 8) | ((Number & 0x1e00) >> 5))
			
			if IsVertical:
				self.Binary[1] = self.Binary[0] & 0xf
				self.Binary[0] &= 0x10
			else:
				self.Binary[1] = 0
			
			self.Binary[2] = 2
			self.Binary[3] = Number & 0xff
			

def ParseLayerIntoObjects(Binary):
	Binary = Binary[5:]
	Objects = []
	while Binary[0] != 0xff:
		Object = SMWObject(Binary)
		Objects.append(Object)
		Binary = Binary[Object.GetSize():]

		# Needed to special out extended object 4 (Map16Reapply) because it does not have a $FF end byte
		if Object.GetNumber() == 0 and Object.GetExtendedNumber() == 0x4:
			break

	return Objects

def EncodeObjectsIntoBinary(Objects):
	Binary = bytearray()
	for Object in Objects:
		Binary += Object.Binary
	return Binary + bytearray([0xff])

def CompressBackgroundImage(Binary):
	Data = bytearray()
	Length = len(Binary)
	i = 0
	Data.extend([Binary[x] for x in range(0, Length // 2, 2)])
	Data.extend([Binary[x] for x in range(Length // 2, Length, 2)])
	Data.extend([Binary[x] for x in range(1, Length // 2, 2)])
	Data.extend([Binary[x] for x in range(1 + Length // 2, Length, 2)])
	Data = RLE1(Data)
	return Data
