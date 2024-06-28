################################################################################
#
# SIX PACK by Ragey
# _map16.py
#
################################################################################

import os
from _snes import *

class Map16:
	def __init__(self, Path):
		with open(Path, 'rb') as File:
			self.Binary = bytearray(File.read())
		self.GraphicOffset = 0x0000B0
		self.ActLikeOffset = 0x0800B0
		self.Assigned = [False] * 0x10000
		self.Verbose = 'Map16 Remap'

		if self.HasTilesetSpecificPage2():
			self.Page2Offset = 0x0900B0
			self.TilesetOffset = 0x0978B0
			self.SpecialOffset = 0x0A68B0
		else:
			self.Page2Offset = None
			self.TilesetOffset = 0x0900B0
			self.SpecialOffset = 0x09F0B0

	def HasTilesetSpecificPage2(self):
		return len(self.Binary) == 682480

	def GetOffsetForSlot(self, Slot, Tileset):
		# Special offset contains the alternative pipes and (for some reason) the overlaid tiles of tilesets 0
		# and 7 as well. Not sure why those are not just emplaced in their respective tilesets instead.
		if Tileset != None and (Tileset == 0 or Tileset == 0x7) and Slot >= 0x1c4 and Slot <= 0x1c7:
			GraphicsOffset = self.SpecialOffset + 0x100 + ((Slot - 0x1c4) * 8)
		elif Tileset != None and (Tileset == 0 or Tileset == 0x7) and Slot >= 0x1ec and Slot <= 0x1ef:
			GraphicsOffset = self.SpecialOffset + 0x120 + ((Slot - 0x1ec) * 8)
		# TODO: Discover the other special tiles and add them here too!
		elif Slot < 0x0200 and Tileset != None:
			GraphicsOffset = self.TilesetOffset + Slot * 8 + Tileset * 0x1000
		elif Slot < 0x0300 and self.Page2Offset != None and Tileset != None:
			GraphicsOffset = self.Page2Offset + (Slot - 0x0200) * 8 + Tileset * 0x800
		else:
			GraphicsOffset = self.GraphicOffset + Slot * 8
		return GraphicsOffset, self.ActLikeOffset + Slot * 2 if Slot < 0x8000 else None

	def GetSlot(self, Slot, Tileset):
		GraphicsOffset, ActLikeOffset = self.GetOffsetForSlot(Slot, Tileset)
		return self.Binary[GraphicsOffset : GraphicsOffset + 8], self.Binary[ActLikeOffset : ActLikeOffset + 2] if Slot < 0x8000 else None

	def ChangeSlot(self, Slot, Graphics, ActLike, Tileset):
		GraphicsOffset, ActLikeOffset = self.GetOffsetForSlot(Slot, Tileset)
		self.Binary[GraphicsOffset : GraphicsOffset + 8] = Graphics
		if Slot < 0x8000:
			self.Binary[ActLikeOffset : ActLikeOffset + 2] = ActLike

	def CompareRangeWith(self, Other, Slot, Until):
		if Slot < 0x8000:
			raise Exception('Only intended to use this with BG tiles!')
		
		Differences = []
		while Slot < Until:
			if not self.TileIsSameAsIn(Other, Slot, None):
				Differences.append(Slot)
			Slot += 1

		return Differences

	def PipeTilesSameAsIn(self, Other):
		for i in range(0, 256):
			if self.Binary[self.SpecialOffset + i] != Other.Binary[Other.SpecialOffset + i]:
				return False
		return True

	def TileIsSameAsIn(self, Other, Slot, Tileset):
		OwnGraphicsOffset, OwnActLikeOffset = self.GetOffsetForSlot(Slot, Tileset)
		OtherGraphicsOffset, OtherActLikeOffset = Other.GetOffsetForSlot(Slot, Tileset)

		OwnGraphics = self.Binary[OwnGraphicsOffset : OwnGraphicsOffset + 8]
		OtherGraphics = Other.Binary[OtherGraphicsOffset : OtherGraphicsOffset + 8]

		if Slot < 0x8000:		
			OwnActLike = self.Binary[OwnActLikeOffset : OwnActLikeOffset + 2]
			OtherActLike = Other.Binary[OtherActLikeOffset : OtherActLikeOffset + 2]
			return OwnGraphics == OtherGraphics and OwnActLike == OtherActLike
		else:
			return OwnGraphics == OtherGraphics

	def FindNextTile(self, Slot):
		if Slot < 0x8000:
			raise Exception('Only intended to use this with BG tiles!')

		while Slot < 0x10000:
			if not self.Assigned[Slot]:
				self.Assigned[Slot] = True
				return Slot
			Slot += 1

		raise 'Map16.FindNextSlot(): No more space available!'

	# Returns Graphics[], ActLike[]
	def GetRectangle(self, Width, Height, Slot, Tileset):
		Width += 1
		Height += 1
		Graphic = [None] * Width
		ActLike = [None] * Width
		for w in range(0, Width):
			Graphic[w] = [None] * Height
			ActLike[w] = [None] * Height
			for h in range(0, Height):
				Slot2 = (h * 16 + w) + Slot
				GraphicOffset, ActLikeOffset = self.GetOffsetForSlot(Slot2, Tileset)
				G, A = self.Binary[GraphicOffset : GraphicOffset + 8], self.Binary[ActLikeOffset : ActLikeOffset + 2]
				Graphic[w][h] = G
				ActLike[w][h] = A
		return Graphic, ActLike

	def Commit(self, Repository):
		for Slot in range(0x200, 0x8000):
			if Repository.Graphics[Slot] != None:
				GraphicOffset, ActLikeOffset = self.GetOffsetForSlot(Slot, None)
				self.Binary[GraphicOffset : GraphicOffset + 8] = Repository.Graphics[Slot]
				self.Binary[ActLikeOffset : ActLikeOffset + 2] = Repository.ActLike[Slot]
				self.Assigned[Slot] = True

# Map16 optimizer
class TileRepository:
	def __init__(self):
		self.Structures = {}
		self.Graphics = [None] * 0x8000
		self.ActLike = [None] * 0x8000
	
	def Add(self, Graphics, ActLike):
		Key = self.Key(Graphics, ActLike)
		self.Structures[Key] = Graphics, ActLike, 0
		return Key
	
	def Key(self, Graphics, ActLike):
		Key = '{:1x}/{:1x}/'.format(len(Graphics) - 1, len(Graphics[0]) - 1)
		for x in range(0, len(Graphics)):
			for y in range(0, len(Graphics[0])):
				Key += '{:04X}.{:04X}.{:04X}.{:04X}:{:04X}/'.format(
					int(Graphics[x][y][1] << 8) | Graphics[x][y][0],
					int(Graphics[x][y][3] << 8) | Graphics[x][y][2],
					int(Graphics[x][y][5] << 8) | Graphics[x][y][4],
					int(Graphics[x][y][7] << 8) | Graphics[x][y][6],
					int(ActLike[x][y][1]) << 8 | int(ActLike[x][y][0]))
		return Key
	
	def Where(self, Key):
		return self.Structures[Key][2]
	
	def Arrange(self):
		n = 0
		for x in range(0, 16)[::-1]:
			for y in range(0, 16)[::-1]:
				for Key in self.Structures:
					if len(self.Structures[Key][0]) == x + 1 and len(self.Structures[Key][0][0]) == y + 1:
						self.__TryCommitCluster(Key)
						n += 1
	
	def __TryCommitCluster(self, Key):
		Graphics = self.Structures[Key][0]
		ActLike = self.Structures[Key][1]
		Width = len(Graphics)
		Height = len(Graphics[0])
		Slot = 0x0200

		while Slot < 0x8000:
			if Width <= 0x10 - (Slot % 16) and self.__TestRectangleAvailable(Graphics, ActLike, Slot):
				self.__WriteTiles(Graphics, ActLike, Slot)
				self.Structures[Key] = self.Structures[Key][0], self.Structures[Key][1], Slot
				return
			Slot += 1
		raise Exception('Could not find a slot for tiles with Key')

	def __TestRectangleAvailable(self, Graphics, ActLike, Slot):
		Width = len(Graphics)
		Height = len(Graphics[0])

		for x in range(0, Width):
			for y in range(0, Height):
				Slot2 = (y * 16 + x) + Slot
				if self.Graphics[Slot2] != None and (self.Graphics[Slot2] != Graphics[x][y] or self.ActLike[Slot2] != ActLike[x][y]):
					return False
		return True
	
	def __WriteTiles(self, Graphics, ActLike, Slot):
		Width = len(Graphics)
		Height = len(Graphics[0])

		for x in range(0, Width):
			for y in range(0, Height):
				Slot2 = (y * 16 + x) + Slot
				self.Graphics[Slot2] = Graphics[x][y]
				self.ActLike[Slot2] = ActLike[x][y]
