###############################################################################
#
# SIX PACK by Ragey <i@ragey.net>
# _stage.py
#
###############################################################################

import os
import copy
from _mwl import *
from _smw import *

###############################################################################

class Stage:
	def __init__(self, Name, SuperMarioWorld):
		self.Name = Name
		self.SuperMarioWorld = SuperMarioWorld
		self.Levels = []
		self.Translevel = None
		self.Verbose = '\n{}\n'.format(self.Name)
		self.OverrideStageName = None
		self.RemapGfx33 = None
		self.MarioLuigiPalette = None

	def AddLevel(self, Level, IsTranslevel):
		self.Levels.append(Level)
		self.Verbose += '\tAdd {} {}'.format(Level.Path, '(Translevel)\n' if IsTranslevel else '\n')

		if IsTranslevel:
			self.Translevel = Level

	def RemoveUnusedLevels(self):
		if self.Translevel == None:
			raise Exception('No translevel assigned to {}'.format(self.Name))

		self.__Traverse(self.Translevel)

		Unused = [Level for Level in self.Levels if Level.Accessible is False and (Level.GetNumber() & 0xff) != 0xc8]
		Prior = len(self.Levels)

		for Level in Unused:
			self.Levels.remove(Level)
			self.Verbose += '\tRemove {}\n'.format(Level.Path)

		return len(Unused)

	def __Traverse(self, Level, Visited = []):
		if Level in Visited:
			return
		
		Visited.append(Level)
		Level.Accessible = True
		Exits = []

		for Object in ParseLayerIntoObjects(Level.GetLayer1()):
			IsSecondary, Number = Object.GetScreenExit()
			if IsSecondary:
				self.__TraverseSecondary(Number, Level, Visited)
			elif IsSecondary == False:
				self.__TraverseLevel(Number, Level, Visited)

	def __TraverseSecondary(self, Number, Level, Visited):
		for Level in self.Levels:
			for Entrance in Level.GetSecondaryEntrancesAsNumbers():
				if Entrance == Number:
					self.__Traverse(Level, Visited)
					return

	def __TraverseLevel(self, Number, Level, Visited):
		for Level in self.Levels:
			if Level.GetNumber() == Number:
				self.__Traverse(Level, Visited)
				return

	def AddReferencedVanillaStages(self, LevelDirectory, PrimaryExits, SecondaryEntrances):
		OwnLevelNumbers = []
		OwnSecondaryEntranceNumbers = []
		OwnSecondaryScreenExits = []
		OwnDirectScreenExits = []
		Count = 0
		
		# Find "native" levels
		for Level in self.Levels:
			OwnLevelNumbers.append(Level.GetNumber())
			OwnSecondaryEntranceNumbers.extend(Level.GetSecondaryEntrancesAsNumbers())
			for Object in ParseLayerIntoObjects(Level.GetLayer1()):
				IsSecondary, Number = Object.GetScreenExit()
				if IsSecondary:
					OwnSecondaryScreenExits.append(Number)
				elif IsSecondary == False:
					OwnDirectScreenExits.append(Number)
		
		# Add vanilla levels that are the result of unaccounted secondary entrances
		AddedLevelNumbers = []
		for Exit in OwnSecondaryScreenExits:
			if Exit not in OwnSecondaryEntranceNumbers and Exit not in AddedLevelNumbers:
				Target = self.SuperMarioWorld.Binary[self.SuperMarioWorld.Secondary05F800 + Exit] | ((self.SuperMarioWorld.Binary[self.SuperMarioWorld.Secondary05FE00 + Exit] & 0x80) >> 3)
				if Target == 0 or Target == 0x100:
					self.Verbose += '\tDirect secondary entrance to bonus level {:3X} was ignored.\n'.format(Exit)
				else:
					AddedLevelNumbers.append(Target)
					self.Verbose += '\t(Direct secondary reference ({:3X})) '.format(Exit)

					L = MarioWorldLevel('{}/_ {:03X}.mwl'.format(LevelDirectory, Target), self.SuperMarioWorld)
					L.AddSecondaryEntrance(Exit, self.SuperMarioWorld)
					self.AddLevel(L, False)
				
		while True:
			NewAddedLevelNumbers = copy.deepcopy(AddedLevelNumbers)
			for Number in AddedLevelNumbers:
				if Number in PrimaryExits:
					for Exit in PrimaryExits[Number]:
						if Exit not in NewAddedLevelNumbers and Exit not in OwnLevelNumbers:
							if Exit == 0 or Exit == 0x100:
								self.Verbose += '\tIndirect secondary entrance to bonus level {:3X} was ignored.\n'.format(Exit)
							else:
								NewAddedLevelNumbers.append(Exit)
								self.Verbose += '\t(Indirect secondary entrance) '
								self.AddLevel(MarioWorldLevel('{}/_ {:03X}.mwl'.format(LevelDirectory, Exit), self.SuperMarioWorld), False)
			if NewAddedLevelNumbers == AddedLevelNumbers:
				break
			AddedLevelNumbers += NewAddedLevelNumbers
			AddedLevelNumbers = list(set(AddedLevelNumbers))

		Count += len(AddedLevelNumbers)
		OwnLevelNumbers += AddedLevelNumbers
		OwnLevelNumbers = list(set(OwnLevelNumbers))

		# Add vanilla levels that are the result of unaccounted primary entrances
		AddedLevelNumbers = []
		for Exit in OwnDirectScreenExits:
			if Exit not in OwnLevelNumbers and Exit not in AddedLevelNumbers:
				if Exit == 0 or Exit == 0x100:
					self.Verbose += '\tDirect primary entrance to bonus level {:3X} was ignored.\n'.format(Exit)
				else:
					AddedLevelNumbers.append(Exit)
					self.Verbose += '\t(Direct primary entrance)'
					self.AddLevel(MarioWorldLevel('{}/_ {:03X}.mwl'.format(LevelDirectory, Exit), self.SuperMarioWorld), False)
		
		while True:
			NewAddedLevelNumbers = copy.deepcopy(AddedLevelNumbers)
			for Number in AddedLevelNumbers:
				if Number in PrimaryExits:
					for Exit in PrimaryExits[Number]:
						if Exit not in NewAddedLevelNumbers and Exit not in OwnLevelNumbers:
							if Exit == 0 or Exit == 0x100:
								self.Verbose += '\tIndirect primary entrance to bonus level {:3X} was ignored.\n'.format(Exit)
							else:
								NewAddedLevelNumbers.append(Exit)
								self.Verbose += '\t(Indirect primary entrance) '
								self.AddLevel(MarioWorldLevel('{}/_ {:03X}.mwl'.format(LevelDirectory, Exit), self.SuperMarioWorld), False)
			if NewAddedLevelNumbers == AddedLevelNumbers:
				break
			AddedLevelNumbers += NewAddedLevelNumbers
			AddedLevelNumbers = list(set(AddedLevelNumbers))
		
		Count += len(AddedLevelNumbers)
		OwnLevelNumbers += AddedLevelNumbers
		OwnLevelNumbers = list(set(OwnLevelNumbers))
	
		return Count

	def RemoveUnusedSecondaryEntrances(self):
		SecondaryScreenExits = []
		for Level in self.Levels:
			for Object in ParseLayerIntoObjects(Level.GetLayer1()):
				IsSecondary, Number = Object.GetScreenExit()
				if IsSecondary:
					SecondaryScreenExits.append(Number)

		SecondaryEntrances = []
		for Level in self.Levels:
			SecondaryEntrances.extend(Level.GetSecondaryEntrancesAsNumbers())

		RemoveCount = 0
		for Entrance in SecondaryEntrances:
			if Entrance not in SecondaryScreenExits:
				for Level in self.Levels:
					if Level.RemoveSecondaryEntranceByNumber(Entrance):
						self.Verbose += '\tRemove secondary entrance {:3X} from level {:3X}\n'.format(Entrance, Level.GetNumber())
						RemoveCount += 1
		
		return len(SecondaryEntrances), RemoveCount

	def RouteYoshiWings(self):
		TargetLevel = None
		HasYoshiWings = False
		
		for Level in self.Levels:
			if Level.OriginalNumber == 0x1c8 and self.Translevel.OriginalNumber >= 0x100:
				TargetLevel = Level
			elif Level.OriginalNumber == 0xc8 and self.Translevel.OriginalNumber < 0x100:
				TargetLevel = Level
		
		for Level in self.Levels:
			if Level.HasYoshiWings():
				HasYoshiWings = True
				if TargetLevel != None:
					Level.AddYoshiWingsExitObject(TargetLevel.GetNumber())
					self.Verbose += '\tLevel {:3X}(->{:3X}) has Yoshi wings pointing to {:3X}(->{:3X})\n'.format(Level.OriginalNumber, Level.GetNumber(), TargetLevel.OriginalNumber, TargetLevel.GetNumber())
				else:
					self.Verbose += '\tLevel {:3X}(->{:3X}) has Yoshi wings but no level for this was provided in the submission.\n'.format(Level.OriginalNumber, Level.GetNumber())
	
		return HasYoshiWings

	def GetGoals(self):
		# Some wrongly detected exits. Most could be fixed by removing invalid exits instead, but doing that would
		# also realign the segments. Which requires me to change the overworld as well. Which I don't want to do.
		if 'VLDC1-031' in self.Name:
			return [False, True]
		elif 'VLDC2-042' in self.Name:
			return [True, False]
		elif 'VLDC2-057' in self.Name:
			return [True, False]
		elif 'VLDC3-SMWC Vanilla LDC 3 [#003]' in self.Name:
			return [True, False]
		elif 'VLDC3-SMWC Vanilla LDC 3 [#013]' in self.Name:
			return [True, False]
		elif 'VLDC3-SMWC Vanilla LDC 3 [#055]' in self.Name:
			return [False, True]
		elif 'VLDC3-SMWC Vanilla LDC 3 [#074]' in self.Name:
			return [True, False]
		elif 'VLDC3-SMWC Vanilla LDC 3 [#103]' in self.Name:
			return [True, False]
		elif 'VLDC4-SMWC Vanilla LDC 4 [#01]' in self.Name:
			return [True, False]
		elif 'VLDC5-46' in self.Name:
			return [False, True]
		elif 'VLDC5-98' in self.Name:
			return [True, False]
		elif 'VLDC5-66' in self.Name:
			return [True, False]

		Goals = [False, False]
		for Level in self.Levels:
			LevelGoals = Level.GetGoals()
			if LevelGoals[0] or LevelGoals[1]:
				self.Verbose += '\tLevel {:3X}(->{:3X}) has Goals: {},{}\n'.format(Level.OriginalNumber, Level.GetNumber(), LevelGoals[0], LevelGoals[1])
			Goals[0] |= LevelGoals[0]
			Goals[1] |= LevelGoals[1]
		
		if Goals[0] == False and Goals[1] == False:
			print('\t', self.Name, 'has no Goals. Setting Goal[0] to True.')
			Goals[0] = True		
		
		return Goals

	def GetInitialSaveFlags(self):
		if self.SuperMarioWorld.Binary[SnesToPc(0x009F19, self.SuperMarioWorld.Mapper)] != 0x22:
			return 0
		else:
			return self.SuperMarioWorld.Binary[SnesToPc(0x05dda0, self.SuperMarioWorld.Mapper) + self.Translevel.OriginalNumber]

	def GetStageName(self):
		if self.OverrideStageName == None:
			return self.SuperMarioWorld.GetLevelName(self.Translevel.OriginalNumber)
		else:
			return self.OverrideStageName

	def HasMessageBoxes(self):
		MessageBoxes = [False, False]
		for Level in self.Levels:
			LevelMessageBoxes = Level.HasMessageBoxes()
			MessageBoxes[0] |= LevelMessageBoxes[0]
			MessageBoxes[1] |= LevelMessageBoxes[1]
		return MessageBoxes

	def GetAuthorName(self):
		if 'VLDC1' in self.Name:
			return Ascii2Smw(self.Name[10 : 10 + self.Name[10:].find('-')].replace('_', '.'), 23)
		elif 'VLDC2' in self.Name: 
			Name = self.Name[11 + self.Name[10:].find('-') : ]
			if Name == 'Chan':
				Name = 'Dokuro-Chan'
			return Ascii2Smw(Name, 23)
		elif 'VLDC3' in self.Name: 
			if 'VLDC3-SMWC Vanilla LDC 3 [#007]' in self.Name:
				return Ascii2Smw('Tails_155', 23)
			if 'VLDC3-SMWC Vanilla LDC 3 [#010]' in self.Name:
				return Ascii2Smw('sky_blue_wiggler', 23)
			Name = self.Name[4 + self.Name.find(' by ') : self.Name.find('[2')]
			return Ascii2Smw(Name[ : Name.find('(')].replace('_', '.'), 23)
		elif 'VLDC4' in self.Name:
			if 'VLDC4-SMWC Vanilla LDC 4 [#34]' in self.Name:
				return Ascii2Smw('limepie20+Argumentable', 23)
			if 'VLDC4-SMWC Vanilla LDC 4 [#08]' in self.Name:
				return Ascii2Smw('horribleTASer1_1', 23)
			if 'VLDC4-SMWC Vanilla LDC 4 [#38]' in self.Name:
				return Ascii2Smw('Blaze_128', 23)
			Name = self.Name[4 + self.Name.find(' by ') : self.Name.find('[2')]
			return Ascii2Smw(Name[ : Name.find('(')].replace('_', '.'), 23)
		elif 'VLDC5' in self.Name:
			return Ascii2Smw(self.Name[1 + self.Name.find('_') : self.Name.find(' - ')].strip().replace('_', '.'), 23)
		elif 'VLDC6' in self.Name: 
			return Ascii2Smw(self.Name[10 : 10 + self.Name[10 :].find('-')].replace('_', '.'), 23)

	def GetAuthorNameAscii(self):
		if 'VLDC1' in self.Name:
			return self.Name[10 : 10 + self.Name[10:].find('-')].replace('_', '.')
		elif 'VLDC2' in self.Name: 
			Name = self.Name[11 + self.Name[10:].find('-') : ]
			if Name == 'Chan':
				Name = 'Dokuro-Chan'
			return Name
		elif 'VLDC3' in self.Name: 
			Name = self.Name[4 + self.Name.find(' by ') : self.Name.find('[2')]
			return Name[ : Name.find('(')].replace('_', '.')
		elif 'VLDC4' in self.Name: 
			Name = self.Name[4 + self.Name.find(' by ') : self.Name.find('[2')]
			return Name[ : Name.find('(')].replace('_', '.')
		elif 'VLDC5' in self.Name:
			return self.Name[1 + self.Name.find('_') : self.Name.find(' - ')].strip().replace('_', '.')
		elif 'VLDC6' in self.Name: 
			return self.Name[10 : 10 + self.Name[10 :].find('-')].replace('_', '.')

	def GetContestNumber(self):
		if 'VLDC1' in self.Name:
			return 0x64
		elif 'VLDC2' in self.Name:
			return 0x65
		elif 'VLDC3' in self.Name:
			return 0x66
		elif 'VLDC4' in self.Name:
			return 0x67
		elif 'VLDC5' in self.Name:
			return 0x68
		elif 'VLDC6' in self.Name:
			return 0x69
