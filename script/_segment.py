###############################################################################
#
# SIX PACK by Ragey <i@ragey.net>
# _segment.py
#
###############################################################################

import struct

###############################################################################

ExcludeLevelNumbers = [0, 0x24, 0xc5, 0xc7, 0xc8, 0x100, 0x1c8]

class Segment():
	def __init__(self):
		self.Translevels = 0
		self.Levels = 0
		self.Stages = []
	
	def TryAddStage(self, Stage):
		if self.Translevels + 2 > 96 - len([x for x in ExcludeLevelNumbers if x <= 0x24 or (x >= 0x101 and x <= 0x13b)]):
			return False
		if self.Levels + len(Stage.Levels) > 512 - 96 - len(ExcludeLevelNumbers):
			return False

		self.Translevels += 1
		self.Levels += len(Stage.Levels) - 1
		self.Stages.append(Stage)
		return True

	def Rearrange(self):
		TranslevelNumber = 1
		LevelNumber = 0x25
		
		for Stage in self.Stages:
			StageLevelNumberMap = {}
			for Level in Stage.Levels:
				OldNumber = Level.GetNumber()

				if Level is Stage.Translevel:
					Level.SetNumber(TranslevelNumber)
					TranslevelNumber += 1
					while TranslevelNumber in ExcludeLevelNumbers:
						TranslevelNumber += 1
					if TranslevelNumber == 0x25:
						TranslevelNumber = 0x101
					if TranslevelNumber > 0x13b:
						raise Exception('Translevel limit exceeded in segment!')
				else:
					Level.SetNumber(LevelNumber)
					LevelNumber += 1
					while LevelNumber in ExcludeLevelNumbers:
						LevelNumber += 1
					if LevelNumber == 0x100:
						LevelNumber = 0x13c
					if LevelNumber > 0x1ff:
						raise Exception('Level limit exceeded in segment!')
				StageLevelNumberMap[OldNumber] = Level.GetNumber()

			Stage.Verbose += '\tLevel remap:  '
			for Key in StageLevelNumberMap:
				Stage.Verbose += '{:X}->{:X}, '.format(Key, StageLevelNumberMap[Key])
			Stage.Verbose = Stage.Verbose[:len(Stage.Verbose)-2] + '\n'
