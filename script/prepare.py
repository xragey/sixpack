################################################################################
#
# SIX PACK by Ragey
# prepare.py
#
# This script will build the Six Pack ROM (and separate Segment ROMs).
# It expects several files to be present and at certain locations.
#
################################################################################

BaseDirectory = 'base'
WorkDirectory = 'work'
InputDirectory = 'input'
OverrideDirectory = 'override'
AmountOfSegments = 8

SourceImageName = 'SuperMarioWorld.smc'
PreparedImageName = 'Prepared.smc'
SixPackImageName = 'SixPack.smc'
DonorImageName = 'Donor.smc'

PathToLunarMagic = 'C:/Program Files (x86)/Lunar Magic/Lunar Magic.exe'
PathToAssembler = 'bin/asar.exe'

################################################################################

import datetime
import filecmp
import functools
import os
import shutil
import subprocess
import sys
from _mwl import *
from _segment import *
from _smw import *
from _stage import *
from _map16 import *
from _palette import *

################################################################################

# Program entry point.
def Main(Arguments):
	PrepareWorkingDirectory()
	if os.path.exists('../{}/{}'.format(BaseDirectory, PreparedImageName)):
		print('[compile.py] Prepared image found, using it!')
		shutil.copyfile('../{}/{}'.format(BaseDirectory, PreparedImageName), '{}'.format(SixPackImageName))
	else:
		PrepareCoreImage()
		ApplyCorePatches()
		input('[compile.py] >>> Change compression to LC_LZ3, then hit return')
		shutil.copyfile('{}'.format(SixPackImageName), '../{}/{}'.format(BaseDirectory, PreparedImageName))
	PrimaryExits, SecondaryEntrances = ComputeDefaultMarioWorldRouting()
	Stages = CreateStageListing()
	RemoveUnusedLevels(Stages)
	RearrangeGraphics(Stages)
	PrepareCustomMarioLuigiPalette(Stages, SuperMarioWorld(SixPackImageName))
	AddReferencesToDefaultLevels(Stages, PrimaryExits, SecondaryEntrances)
	RemoveUnusedSecondaryEntrances(Stages)
	RemoveCustomMusicReferences(Stages)
	RearrangeForegroundMap16(Stages)
	RearrangeBackgroundMap16(Stages)
	subprocess.call([PathToLunarMagic, '-ImportAllMap16', SixPackImageName, 'SixPack.map16'])
	Branch()
	ApplySixPackPatches()
	Segments = RearrangeIdentifiers(Stages)
	Create(Segments, Stages)
	Register()
	WriteVerboseOutput(Stages)

# Clears and (re)creates the working directory and moves into it.
def PrepareWorkingDirectory():
	print('[compile.py] Preparing work directory...')
	shutil.rmtree(WorkDirectory, ignore_errors = True)
	os.mkdir(WorkDirectory)
	os.chdir('./{}'.format(WorkDirectory))
	shutil.copytree('../{}/Graphics'.format(BaseDirectory), 'Graphics')
	shutil.copytree('../{}/ExGraphics'.format(BaseDirectory), 'ExGraphics')
	shutil.copyfile('../{}/all.map16'.format(BaseDirectory), 'SixPack.map16')

# Convert a clean SMW image into a prepared image. Installs SA-1 pack, Lunar Magic ASM, and custom music.
def PrepareCoreImage():
	print('[compile.py] Preparing core image...')
	shutil.copyfile('../{}/{}'.format(BaseDirectory, SourceImageName), '{}'.format(SixPackImageName))
	subprocess.call([PathToLunarMagic, '-ExpandROM', SixPackImageName, '2MB'])
	subprocess.call(['../{}'.format(PathToAssembler), '../asm/sa1/sa1.asm', SixPackImageName])
	subprocess.call([PathToLunarMagic, '-ExpandROM', SixPackImageName, '8MB_SA1'])
	subprocess.call(['../{}'.format(PathToAssembler), '../asm/reserve.asm', SixPackImageName])
	subprocess.call([PathToLunarMagic, '-ImportGFX', SixPackImageName])
	subprocess.call([PathToLunarMagic, '-ExportExGFX', SixPackImageName])
	subprocess.call([PathToLunarMagic, '-ImportExGFX', SixPackImageName])
	subprocess.call([PathToLunarMagic, '-ImportLevel', SixPackImageName, '../{}/InstallLunarMagicASM.mwl'.format(BaseDirectory)])
	os.chdir('../music')
	subprocess.call(['./AddmusicK.exe', '-noblock', '../{}/{}'.format(WorkDirectory, SixPackImageName)])
	os.chdir('../work')
	os.remove('SixPack.msc')
	os.remove('SixPack.smc~')

# Applies the patches that apply to both SixPack.sfc and the Segment_.sfc images.
def ApplyCorePatches():
	print('[compile.py] Applying core patches...')
	subprocess.call(['../{}'.format(PathToAssembler), '../asm/autofeatherfreeze.asm', SixPackImageName])
	subprocess.call(['../{}'.format(PathToAssembler), '../asm/bonusgame.asm', SixPackImageName])
	subprocess.call(['../{}'.format(PathToAssembler), '../asm/bowser.asm', SixPackImageName])
	subprocess.call(['../{}'.format(PathToAssembler), '../asm/creatingblock.asm', SixPackImageName])
	subprocess.call(['../{}'.format(PathToAssembler), '../asm/dragoncoin.asm', SixPackImageName])
	subprocess.call(['../{}'.format(PathToAssembler), '../asm/lightning.asm', SixPackImageName])
	subprocess.call(['../{}'.format(PathToAssembler), '../asm/lineguideactfix.asm', SixPackImageName])
	subprocess.call(['../{}'.format(PathToAssembler), '../asm/logo.asm', SixPackImageName])
	subprocess.call(['../{}'.format(PathToAssembler), '../asm/midway.asm', SixPackImageName])
	subprocess.call(['../{}'.format(PathToAssembler), '../asm/misc.asm', SixPackImageName])
	subprocess.call(['../{}'.format(PathToAssembler), '../asm/tilegen.asm', SixPackImageName])
	subprocess.call(['../{}'.format(PathToAssembler), '../asm/title.asm', SixPackImageName])
	subprocess.call(['../{}'.format(PathToAssembler), '../asm/remap16.asm', SixPackImageName])
	subprocess.call(['../{}'.format(PathToAssembler), '../asm/scrollcrash.asm', SixPackImageName])
	subprocess.call(['../{}'.format(PathToAssembler), '../asm/sideways.asm', SixPackImageName])
	subprocess.call(['../{}'.format(PathToAssembler), '../asm/tally.asm', SixPackImageName])
	subprocess.call(['../{}'.format(PathToAssembler), '../asm/palcompress.asm', SixPackImageName])
	subprocess.call(['../{}'.format(PathToAssembler), '../asm/palace.asm', SixPackImageName])
	subprocess.call(['../{}'.format(PathToAssembler), '../asm/piranha.asm', SixPackImageName])
	subprocess.call(['../{}'.format(PathToAssembler), '../asm/pswitch.asm', SixPackImageName])
	subprocess.call(['../{}'.format(PathToAssembler), '../asm/wings.asm', SixPackImageName])
	subprocess.call(['../{}'.format(PathToAssembler), '../asm/yoshi.asm', SixPackImageName])
	subprocess.call([PathToLunarMagic, '-TransferOverworld', SixPackImageName, '../{}/{}'.format(BaseDirectory, DonorImageName)])
	subprocess.call([PathToLunarMagic, '-TransferTitleScreen', SixPackImageName, '../{}/{}'.format(BaseDirectory, DonorImageName)])
	subprocess.call(['../{}'.format(PathToAssembler), '../asm/gfx33.asm', SixPackImageName])
	subprocess.call(['../{}'.format(PathToAssembler), '../asm/save.asm', SixPackImageName])
	subprocess.call(['../{}'.format(PathToAssembler), '../asm/messages.asm', SixPackImageName])
	subprocess.call(['../{}'.format(PathToAssembler), '../asm/owdisplay.asm', SixPackImageName])
	subprocess.call(['../{}'.format(PathToAssembler), '../asm/owprogress.asm', SixPackImageName])

# Applies the patches that should be applied only to SixPack.sfc and not to the Segment_.sfc images.
def ApplySixPackPatches():
	print('[compile.py] Applying SixPack-specific patches...')
	subprocess.call(['../{}'.format(PathToAssembler), '../asm/demo.asm', SixPackImageName])
	subprocess.call(['../{}'.format(PathToAssembler), '../asm/pointer.asm', SixPackImageName])
	subprocess.call(['../{}'.format(PathToAssembler), '../asm/warning.asm', SixPackImageName])
	subprocess.call(['../{}'.format(PathToAssembler), '../asm/owpalette.asm', SixPackImageName])
	subprocess.call(['../{}'.format(PathToAssembler), '../asm/mariopalette.asm', SixPackImageName])

# Creates the Segment_.sfc images from the current state of the SixPack.sfc image.
def Branch():
	print('[compile.py] Creating segment images...')
	for i in range(0, 8):
		shutil.copyfile(SixPackImageName, 'Segment{}.smc'.format(i))

# Computes the links between levels in the vanilla games. Most contest entries will only reuse vanilla boss stages, but some
# entries (presumably by accident) allow entry into regular vanilla stages. These may link to other vanilla stages, so the
# entire sequence must be carried over. The mapping returned by this function is used for that.
# Returns {} of Level ID -> Level IDs it goes into, {} of Exit ID -> Level ID it points to.
def ComputeDefaultMarioWorldRouting():
	print('[compile.py] Mapping default game routes...')
	Levels = []
	for FileName in os.listdir('../{}/level'.format(BaseDirectory)):
		FilePath = os.path.join('../{}/level'.format(BaseDirectory), FileName)
		if not os.path.isfile(FilePath):
			continue
		Levels.append(MarioWorldLevel(FilePath, None))

	SecondaryEntrances = {}
	for Level in Levels:
		for Entrance in Level.GetSecondaryEntrancesAsNumbers():
			SecondaryEntrances[Entrance] = Level.GetNumber()

	PrimaryExits = {}
	for Level in Levels:
		Routes = []
		for Exit in Level.GetScreenExits():
			Routes.append(Exit[1] if Exit[0] == False else SecondaryEntrances[Exit[1]])
		if len(Routes) > 0:
			PrimaryExits[Level.GetNumber()] = list(set(Routes))

	print('[compile.py]     Prepared {} routes!'.format(len(PrimaryExits)))
	print('[compile.py]     Found {} secondary paths!'.format(len(SecondaryEntrances)))

	return PrimaryExits, SecondaryEntrances 

# Reads all the input stages and returns them in as a List of Stage objects.
def CreateStageListing():
	print('[compile.py] Creating stage listing from input files...')
	SourceGamesDirectory = '../{}/rom'.format(InputDirectory)
	SourceLevelsDirectory = '../{}/mwl'.format(InputDirectory)
	OverrideLevelsDirectory = '../{}/mwl'.format(OverrideDirectory)

	with open('../{}/translevels.txt'.format(InputDirectory)) as File:
		Contents = File.read().splitlines()
		TransLevelNames = [Line.split(':')[0] for Line in Contents]

	with open('../{}/demo.txt'.format(InputDirectory)) as File:
		DemoReelNames = [Line.split(':')[0] for Line in File.read().splitlines()]

	OverrideStageNames = {}
	for i in range(0, len(TransLevelNames)):
		Split = Contents[i].split(':')
		OverrideStageNames[Split[0]] = Split[1] if len(Split) > 1 else None

	Stages = []
	CurrentName = None

	for FileName in os.listdir(SourceLevelsDirectory):
		Path = os.path.join(SourceLevelsDirectory, FileName)

		if not os.path.isfile(Path) or FileName == '.gitkeep':
			continue

		if CurrentName != FileName[:len(FileName)-8]:
			CurrentName = FileName[0:len(FileName)-8]
			Source = SuperMarioWorld('{}/{}.smc'.format(SourceGamesDirectory, CurrentName))			
			CurrentStage = Stage(CurrentName, Source)
			Stages.append(CurrentStage)
		
		OverridePath = os.path.join(OverrideLevelsDirectory, FileName)	
		Level = MarioWorldLevel(OverridePath if os.path.isfile(OverridePath) else Path, Source)
		
		if FileName in DemoReelNames:
			Level.InDemoReel = True

		CurrentStage.AddLevel(Level, FileName in TransLevelNames)
		if FileName in TransLevelNames:
			CurrentStage.OverrideStageName = Ascii2Smw(OverrideStageNames[FileName], 19) if OverrideStageNames[FileName] != None else None

	CountLevels = functools.reduce(lambda Left, Right: Left + Right, [len(Stage.Levels) for Stage in Stages], 0)
	print('[compile.py]     Read {} stages and {} levels!'.format(len(Stages), CountLevels))
	return Stages

# Many entries include altered levels that cannot actually be reached from the provided translevel. This function removes
# those levels from the repository to save space in the target ROM.
def RemoveUnusedLevels(Stages):
	print('[compile.py] Scanning for unused levels...')
	Count = 0
	for Stage in Stages:
		Count += Stage.RemoveUnusedLevels()
	print('[compile.py]     Removed {} levels!'.format(Count))

# Apply references to default levels (if any) to the stages. Note that Lunar Magic will not extract unchanged levels by
# default, so they're not in the repository. This will add them back in.
def AddReferencesToDefaultLevels(Stages, PrimaryExits, SecondaryEntrances):
	print('[compile.py] Adding referenced default levels...')
	Count = 0
	for Stage in Stages:
		Count += Stage.AddReferencedVanillaStages('../{}/level'.format(BaseDirectory), PrimaryExits, SecondaryEntrances)
	print('[compile.py]     Added {} levels!'.format(Count))

# As the function title says ;)
def RemoveUnusedSecondaryEntrances(Stages):
	print('[compile.py] Scanning for unused secondary entrances...')
	Count = 0
	Removed = 0
	for Stage in Stages:
		C, R = Stage.RemoveUnusedSecondaryEntrances()
		Count += C
		Removed += R
	print('[compile.py]     Removed {} secondary entrances of {}!'.format(Removed, Count))
	if Count - Removed > 0x4FF:
		print('[compile.py]     WARNING! More secondary entrances remain than the expected 0x4FF!')

def RemoveCustomMusicReferences(Stages):
	print('[compile.py] Scanning for custom music references...')
	Count = 0
	for Stage in Stages:
		for Level in Stage.Levels:
			Level.NormalizeTime()
			if Level.RemoveMusicBypass():
				Stage.Verbose += '\tRemove custom music object from {:3X}\n'.format(Level.GetNumber())
				Count += 1
	print('[compile.py]     Removed custom music from {} levels!'.format(Count))

# Remaps level numbers, exit numbers, and entrance numbers to arrange them into Segments. Each Segment has the same limits as
# a standard Super Mario World image; a maximum of 96 translevels and 512 levels overall.
def RearrangeIdentifiers(Stages):
	print('[compile.py] Distributing levels over segments...')
	SecondaryEntranceNumber = 1
	Segments = [Segment()]
	CurrentSegment = Segments[0]

	for Stage in Stages:
		while not CurrentSegment.TryAddStage(Stage):
			print('[compile.py]     Segment {}: {:3} levels and {:2} translevels'.format(len(Segments) - 1, CurrentSegment.Levels, CurrentSegment.Translevels))
			Segments.append(Segment())
			CurrentSegment = Segments[len(Segments) - 1]
	print('[compile.py]     Segment {}: {:3} levels and {:2} translevels'.format(len(Segments) - 1, CurrentSegment.Levels, CurrentSegment.Translevels))

	print('[compile.py] Assigning new identifiers to stages....')
	for S in Segments:
		TranslevelNumber = 1
		LevelNumber = 0x25

		for Stage in S.Stages:
			StageSecondaryEntranceMap = {}
			for Level in Stage.Levels:
				SecondaryEntranceNumber = Level.RemapSecondaryEntrances(SecondaryEntranceNumber, StageSecondaryEntranceMap)
		
			StageLevelNumberMap = {}
			for Level in Stage.Levels:
				OldNumber = Level.GetNumber()

				if Level is Stage.Translevel:
					# This level uses a trick to access more messages in a single level using sprite 0x19
					if 'VLDC4-SMWC Vanilla LDC 4 [#60] - Gravity Castle' in Stage.Name:
						Level.SetNumber(0x138)
					else:
						Level.SetNumber(TranslevelNumber)
					TranslevelNumber += 1
					while TranslevelNumber in ExcludeLevelNumbers:
						TranslevelNumber += 1
					if TranslevelNumber >= 0x25 and TranslevelNumber <= 0x100:
						TranslevelNumber = 0x101
					if TranslevelNumber > 0x13b:
						raise Exception('Translevel limit exceeded in segment!')
				else:
					Level.SetNumber(LevelNumber)
					LevelNumber += 1
					while LevelNumber in ExcludeLevelNumbers:
						LevelNumber += 1
					if LevelNumber >= 0x100 and LevelNumber <= 0x13b:
						LevelNumber = 0x13c
					if LevelNumber > 0x1ff:
						raise Exception('Level limit exceeded in segment!')
				StageLevelNumberMap[OldNumber] = Level.GetNumber()
			
			for Level in Stage.Levels:		
				T = Level.RemapScreenExits(StageLevelNumberMap, StageSecondaryEntranceMap)
				if len(T) > 0:
					Stage.Verbose += '\tScreen exit remap for Level ({:X}->{:X}):  '.format(Level.OriginalNumber, Level.GetNumber())
					for Key in T:
						Stage.Verbose += '[{}{:X}->{:X}], '.format('*s*' if Key[1] else '', Key[0], T[Key])
					Stage.Verbose = Stage.Verbose[:len(Stage.Verbose)-2] + '\n'

			Stage.Verbose += '\tLevel remap:  '
			if len(StageLevelNumberMap) > 0:
				for Key in StageLevelNumberMap:
					Stage.Verbose += '{:X}->{:X}, '.format(Key, StageLevelNumberMap[Key])
				Stage.Verbose = Stage.Verbose[:len(Stage.Verbose)-2] + '\n'

			Stage.Verbose += '\tSecondary entrance remap: '
			if len(StageSecondaryEntranceMap) > 0:
				for Key in StageSecondaryEntranceMap:
					Stage.Verbose += '{:X}->{:X}, '.format(Key, StageSecondaryEntranceMap[Key])
				Stage.Verbose = Stage.Verbose[:len(Stage.Verbose)-2]
			Stage.Verbose += '\n'

	CountYoshiWings = 0
	for Stage in Stages:
		CountYoshiWings += Stage.RouteYoshiWings()
	print('[compile.py]     Handled Yoshi wing routing for {} stages!'.format(CountYoshiWings))

	return Segments

# Gets rid of unused graphics files and rearranges the used ones.
def RearrangeGraphics(Stages):
	print('[compile.py] Scan and rearrange graphics...')
	ExGFX = 0x0094
	ExGFXReserved = 0x0088

	# Enable modern graphics bypass in all levels. This makes further processing easier.
	Count = 0
	for Stage in Stages:
		for Level in Stage.Levels:
			# Don't enable bypass in boss levels unless the author bypassed it themselves
			if Level.IsBossLevel():
				continue
			Enabled, SpriteListIndex, BlockListIndex = Level.EnableGraphicsBypass()
			if Enabled:
				Count += 1
				Stage.Verbose += '\tEnable graphics bypass for level {:3X}\n'.format(Level.GetNumber())

				if SpriteListIndex > 0 or BlockListIndex > 0:
					Stage.Verbose += '\t\tThis stage was using the old bypass system ({:2X},{:2X})\n'.format(SpriteListIndex, BlockListIndex)
	print('[compile.py]     Enabled graphics bypass in {} levels'.format(Count))

	for Stage in Stages:
		StageGFXFiles = set()

		for Level in Stage.Levels:
			if not Level.IsGraphicsBypassEnabled():
				continue
			
			StageGFXFiles = StageGFXFiles.union(Level.GetGraphicsBypassNumbers())

		# We already removed unused levels, so all remaining ExGFX references are used.
		StageGFXMap = {}	
		StageGFXToChange = [N for N in StageGFXFiles if N > 0x7f]
		
		# Check the last 3kB of GFX00.
		# Skip the first 1kB because people often put their own name over the "Nintendo Presents" graphic.
		# -- TODO --

		# Check GFX01 twice; how this file looks for each entry depends on how the berry tile was exported.
		Current = '../{}/gfx/{}/Graphics/GFX01.bin'.format(InputDirectory, Stage.Name)
		if not (filecmp.cmp(Current, '../{}/BaseGraphics/GFX01.bin'.format(BaseDirectory), False) or filecmp.cmp(Current, '../{}/BaseGraphics/GFX01-AltBerry.bin'.format(BaseDirectory), False)):
			StageGFXToChange.append(0x01)
		
		# Check GFX02--GFX26.
		for Index in [*range(2, 0x26)] + [0x27, 0x2c, 0x2d, 0x2e, 0x2f, 0x30, 0x31]:
			if Index in StageGFXFiles:
				Current = '../{}/gfx/{}/Graphics/GFX{:02X}.bin'.format(InputDirectory, Stage.Name, Index)
				if not filecmp.cmp(Current, '../{}/BaseGraphics/GFX{:02X}.bin'.format(BaseDirectory, Index), False):
					StageGFXToChange.append(Index)

		Index = 0x33
		Current = '../{}/gfx/{}/Graphics/GFX{:02X}.bin'.format(InputDirectory, Stage.Name, Index)
		if not filecmp.cmp(Current, '../{}/Graphics/GFX{:02X}.bin'.format(BaseDirectory, Index), False):
			if ExGFXReserved >= 0x0094:
				raise Exception('ExGFXReserved crossed maximum, change script!')
			StageGFXMap = {0x33: ExGFXReserved}
			#print('{}: Remap 0x33->0x{:3X}'.format(Stage.Name, ExGFXReserved))
			Stage.RemapGfx33 = ExGFXReserved
			ExGFXReserved += 1

		for Level in Stage.Levels:
			if not Level.IsGraphicsBypassEnabled():
				Stage.Verbose += '\n\tDid NOT remap graphics for level {:3X} because it was not ExGFX-enabled\n'.format(Level.GetNumber())
				continue

			OldExGFX = ExGFX
			ExGFX = Level.RemapGraphicsBypass(ExGFX, StageGFXToChange, StageGFXMap)
			if OldExGFX != ExGFX:
				Stage.Verbose += '\n\tRemapped {} graphics for level {:3X}\n'.format(ExGFX - OldExGFX, Level.GetNumber())
		
		for Key in StageGFXMap:
			try:
				if Key > 0x7f:
					shutil.copyfile('../{}/gfx/{}/ExGFX{:02X}.bin'.format(InputDirectory, Stage.Name, Key), 'ExGraphics/ExGFX{:02X}.bin'.format(StageGFXMap[Key]))
				else:
					shutil.copyfile('../{}/gfx/{}/Graphics/GFX{:02X}.bin'.format(InputDirectory, Stage.Name, Key), 'ExGraphics/ExGFX{:02X}.bin'.format(StageGFXMap[Key]))
			except:
				#print('[compile.py]     {} referenced GFX {:3X} which is not present in the source ROM'.format(Stage.Name, Key))
				Stage.Verbose += '\tRemoved graphic {:3X} from all levels because it was not present in the source ROM\n'.format(StageGFXMap[Key], Level.GetNumber())
				for Level in Stage.Levels:
					if not Level.IsGraphicsBypassEnabled():
						continue
					Level.RemoveGraphicsBypass(StageGFXMap[Key])

	print('[compile.py]     Remap done, retained {} (Ex)GFX files, last index is {:03X}!'.format(ExGFX - 0x0080, ExGFX - 1))
	subprocess.call([PathToLunarMagic, '-ImportExGFX', SixPackImageName])

def PrepareCustomMarioLuigiPalette(Stages, Game):
	Count = 0
	for Stage in Stages:
		Stage.MarioLuigiPalette = Stage.SuperMarioWorld.GetCustomMarioLuigiPalette(Game)
		if Stage.MarioLuigiPalette is not None:
			Count += 1
	print('[compile.py]     {} stages define a custom global palette for Mario and Luigi.'.format(Count))

def RearrangeForegroundMap16(Stages):
	print('[compile.py] Rearranging foreground Map16...')
	WorkMap16 = Map16('SixPack.map16')
	Repository = TileRepository()

	for Stage in Stages:
		OverridePath = '../{}/map16/{}.map16'.format(OverrideDirectory, Stage.Name)
		Path = '../{}/map16/{}.map16'.format(InputDirectory, Stage.Name)
		StageMap16 = Map16(OverridePath if os.path.isfile(OverridePath) else Path)
		
		#if not StageMap16.PipeTilesSameAsIn(WorkMap16):
		#	print('!! {} has different pipe tiles'.format(Stage.Name))
	
		for Level in Stage.Levels:
			Collection = {}
			for Tile in range(0, 0x200):
				if not StageMap16.TileIsSameAsIn(WorkMap16, Tile, Level.GetTileset()):
					Collection[Tile] = (0, 0, Level.GetTileset())
			Level.GetForegroundDirectMap16(Collection)

			for Tile in Collection.copy():
				if Tile < 0x200 and StageMap16.TileIsSameAsIn(WorkMap16, Tile, Collection[Tile][2]):
					Collection.pop(Tile)
			
			# For switch tiles, also copy the other entity
			for Tile in [0x6a, 0x6b, 0x6c, 0x6d]:
				if (Tile in Collection) and ((Tile + 0x100) not in Collection):
					Collection[(Tile + 0x100)] = (0, 0, Level.GetTileset())
				elif (Tile not in Collection) and ((Tile + 0x100) in Collection):
					Collection[(Tile)] = (0, 0, Level.GetTileset())

			for Tile in Collection:
				# Dynamic pipe tiles are handled by manual remap
				if Tile >= 0x133 and Tile <= 0x13a:
					continue

				Width = Collection[Tile][0]
				Height = Collection[Tile][1]
				Tileset = Collection[Tile][2]
				Graphics, ActLike = StageMap16.GetRectangle(Width, Height, Tile, Tileset)
				Key = Repository.Add(Graphics, ActLike)

	print('[compile.py]     Arranging foreground Map16... this may take awhile...')
	Repository.Arrange()

	print('[compile.py]     Done! Building Map16 data now.')
	WorkMap16.Commit(Repository)

	for Stage in Stages:
		OverridePath = '../{}/map16/{}.map16'.format(OverrideDirectory, Stage.Name)
		Path = '../{}/map16/{}.map16'.format(InputDirectory, Stage.Name)
		StageMap16 = Map16(OverridePath if os.path.isfile(OverridePath) else Path)

		for Level in Stage.Levels:
			ChangeMap = {}
			Collection = {}
			for Tile in range(0, 0x200):
				if not StageMap16.TileIsSameAsIn(WorkMap16, Tile, Level.GetTileset()):
					Collection[Tile] = (0, 0, Level.GetTileset())
			Level.GetForegroundDirectMap16(Collection)

			for Tile in Collection.copy():
				if Tile < 0x200 and StageMap16.TileIsSameAsIn(WorkMap16, Tile, Collection[Tile][2]):
					Collection.pop(Tile)

			# For switch tiles, also copy the other entity
			for Tile in [0x6a, 0x6b, 0x6c, 0x6d]:
				if (Tile in Collection) and ((Tile + 0x100) not in Collection):
					Collection[(Tile + 0x100)] = (0, 0, Level.GetTileset())
				elif (Tile not in Collection) and ((Tile + 0x100) in Collection):
					Collection[(Tile)] = (0, 0, Level.GetTileset())

			for Tile in Collection:
				# Dynamic pipe tiles are handled by manual remap
				if Tile >= 0x133 and Tile <= 0x13a:
					continue

				Width = Collection[Tile][0]
				Height = Collection[Tile][1]
				Tileset = Collection[Tile][2]
				Graphics, ActLike = StageMap16.GetRectangle(Width, Height, Tile, Tileset)
				ChangeMap[Tile] = Repository.Where(Repository.Key(Graphics, ActLike))

			LowMap16Remap = {k:v for (k,v) in ChangeMap.items() if k < 0x200}
			if len(LowMap16Remap) > 0:
				Stage.Verbose += '\tApplying low Map16 remap to {:3X} ({} tiles)\n'.format(Level.OriginalNumber, str(len(LowMap16Remap)))
				Stage.Verbose += '\t\t'
				for Key in LowMap16Remap:
					Stage.Verbose += '{:4X}->{:4X}, '.format(Key, LowMap16Remap[Key])
				Stage.Verbose += '\n'

			Level.RemapForegroundDirectMap16(ChangeMap)
			Level.ApplyMap16RemapObject(LowMap16Remap)

	with open('SixPack.map16', 'wb') as File:
		File.write(WorkMap16.Binary)

def RearrangeBackgroundMap16(Stages):
	print('[compile.py] Rearranging background Map16...')

	BaseMap16 = Map16('../{}/all.map16'.format(BaseDirectory))
	WorkMap16 = Map16('SixPack.map16')
	Slot = 0x8200

	for Stage in Stages:
		OverridePath = '../{}/map16/{}.map16'.format(OverrideDirectory, Stage.Name)
		Path = '../{}/map16/{}.map16'.format(InputDirectory, Stage.Name)
		StageMap16 = Map16(OverridePath if os.path.isfile(OverridePath) else Path)

		Differences = BaseMap16.CompareRangeWith(StageMap16, 0x8000, 0x8200)

		TilesToCopy = []
		for Level in Stage.Levels:
			TilesToCopy = list(set(TilesToCopy + Level.GetBackgroundTilemap()))
		TilesToCopy = [Tile for Tile in TilesToCopy if Tile >= 0x8200 or (Tile in Differences)]

		if Slot < 0x9000 and Slot + len(TilesToCopy) >= 0x9000:
			Stage.Verbose += '\tSwitched background Map16 bank to $09\n'
			Slot = 0x9200

		ChangeMap = {}
		for Tile in TilesToCopy:
			Graphics, ActLike = StageMap16.GetSlot(Tile, None)
			Slot = WorkMap16.FindNextTile(Slot)
			WorkMap16.ChangeSlot(Slot, Graphics, ActLike, None)
			ChangeMap[Tile] = Slot

		Stage.Verbose += '\tApplying background map16 remap: '
		for Key in ChangeMap:
			Stage.Verbose += '{:4X}->{:4X}, '.format(Key, ChangeMap[Key])
		Stage.Verbose += '\n'

		for Level in Stage.Levels:
			if not Level.Layer2IsForeground():
				Level.RemapBackgroundTilemap(ChangeMap, Slot > 0x9000)

	with open('SixPack.map16', 'wb') as File:
		File.write(WorkMap16.Binary)

# Creates SixPack.sfc and separate Segment_.sfc files. The segment files are used for verifying the output as they can be opened
# and viewed in Lunar Magic and other tools. Because SixPack.sfc moves pointers around, it can only be played, but not viewed in
# standard editors.
def Create(Segments, Stages):
	PalCompress = CompressPalettes(Stages)
	BonusLevels = [MarioWorldLevel('../base/level/_ 000.mwl', None), MarioWorldLevel('../base/level/_ 0C8.mwl', None), MarioWorldLevel('../base/level/_ 100.mwl', None), MarioWorldLevel('../base/level/_ 1C8.mwl', None)]
	TotalGoalCount = 0

	Game = SuperMarioWorld(SixPackImageName)
	Game.SixPackPointers()
	Game.SetDefaultMessages()
	Game.SetMessageForLevel(0, 0, Ascii2Smw("                                         SIX PACK                            by Ragey", 18 * 8 + 1))
	Game.SetMessageForLevel(0, 1, Ascii2Smw("                                                                        Several  levels inthis   compilationcontain   flashingcolors and images.", 18 * 8 + 1))

	Authors = set()

	print('[compile.py] Creating output files...')
	for SegmentNumber in range(0, AmountOfSegments):
		S = Segments[SegmentNumber]
		SubGame = SuperMarioWorld('Segment{}.smc'.format(SegmentNumber))
		SubGame.SetDefaultMessages()

		for Level in BonusLevels:
			PalCompress.Add(Level.GetPalette())
			Level.SetCompressedPalette(PalCompress.Get(Level.GetPalette()))
			Game.InsertLevel(Level, SegmentNumber * 0x200)

		for Stage in S.Stages:
			Game.InsertGfx33User(Stage, SegmentNumber * 0x200)
			IDx = Game.InsertCustomMarioLuigiPalette(Stage, SegmentNumber * 0x200)
			Stage.Translevel.AddMarioLuigiPaletteObject(IDx)
			SubGame.InsertGfx33User(Stage, 0)

			for Level in Stage.Levels:
				Game.InsertLevel(Level, SegmentNumber * 0x200)
				SubGame.InsertLevel(Level, 0)			
				if Level.InDemoReel:
					Game.AddToDemoReel(Level, SegmentNumber * 0x200)
			Stage.Verbose += '\tInsert into Segment {}@{:3X}\n'.format(SegmentNumber, Stage.Translevel.GetNumber())
			if 'VLDC2-064-SMWorldbound-TLMB' in Stage.Name:
				TransNumber = NumberToTransIndex(Stage.Translevel.GetNumber() + 0x200 * SegmentNumber)
				print('[compile.py]     Stage that has midway enabled by default {}@{:X} (Index {:X}) (Should be C5)'.format(SegmentNumber, Stage.Translevel.GetNumber(), TransNumber))
			elif 'VLDC2-047-Trip to Yoshi' in Stage.Name:
				TransNumber = NumberToTransIndex(Stage.Translevel.GetNumber() + 0x200 * SegmentNumber)
				print('[compile.py]     Stage that exits by sideways exit {}@{:X} (Index {:X}) (Should be 77)'.format(SegmentNumber, Stage.Translevel.GetNumber(), TransNumber))
			if Stage.SuperMarioWorld.PiranhaProperty() != 0xb:
				TransNumber = NumberToTransIndex(Stage.Translevel.GetNumber() + 0x200 * SegmentNumber)
				print('[compile.py]     Stage that has 0xa as its piranha plant byte {}@{:X} (Index {:X}) (Should be C6 and 18C)'.format(SegmentNumber, Stage.Translevel.GetNumber(), TransNumber))
			if 'VLDC6-060' in Stage.Name:
				TransNumber = NumberToTransIndex(Stage.Translevel.GetNumber() + 0x200 * SegmentNumber)
				print('[compile.py]     Stage that exits by bonus game {}@{:X} (Index {:X}) (Should be 2E6)'.format(SegmentNumber, Stage.Translevel.GetNumber(), TransNumber))
			if 'VLDC6-071' in Stage.Name:
				TransNumber = NumberToTransIndex(Stage.Translevel.GetNumber() + 0x200 * SegmentNumber)
				print('[compile.py]     Stage that saves Dragon coins {}@{:X} (Index {:X}) (Should be 2F1)'.format(SegmentNumber, Stage.Translevel.GetNumber(), TransNumber))

			# This level uses a trick to access more messages in a single level using sprite 0x19
			if 'VLDC4-SMWC Vanilla LDC 4 [#60] - Gravity Castle' in Stage.Name:
				for i in range(0, 7):
					if i == 2:
						Message = Stage.SuperMarioWorld.GetMessageForLevel(0, 1, None)
					else:
						Message = Stage.SuperMarioWorld.GetMessageForLevel(Stage.Translevel.OriginalNumber + (i // 2), i % 2, None)
					SubGame.SetMessageForLevel(0x138 + (i // 2), i % 2, Message)
					Game.SetMessageForLevel(0x138 + (SegmentNumber * 0x200) + (i // 2), i % 2, Message)
			# Same here, but the next entry in Six Pack doesn't have its own messages, so no level remap is needed
			elif 'VLDC4-SMWC Vanilla LDC 4 [#32]' in Stage.Name:
				Message = Stage.SuperMarioWorld.GetMessageForLevel(Stage.Translevel.OriginalNumber, 0, None)
				SubGame.SetMessageForLevel(Stage.Translevel.GetNumber(), 0, Message)
				Game.SetMessageForLevel(Stage.Translevel.GetNumber() + (SegmentNumber * 0x200), 0, Message)
				Message = Stage.SuperMarioWorld.GetMessageForLevel(Stage.Translevel.OriginalNumber, 1, None)
				SubGame.SetMessageForLevel(Stage.Translevel.GetNumber(), 1, Message)
				Game.SetMessageForLevel(Stage.Translevel.GetNumber() + (SegmentNumber * 0x200), 1, Message)
				Message = Stage.SuperMarioWorld.GetMessageForLevel(0, 1, None)
				SubGame.SetMessageForLevel(Stage.Translevel.GetNumber() + 1, 0, Message)
				Game.SetMessageForLevel(Stage.Translevel.GetNumber() + 1 + (SegmentNumber * 0x200), 0, Message)
			# This level is provided as a broken ROM and apparently the script can't find the messages in those, so we add them manually.
			elif 'VLDC6-077' in Stage.Name:
				Message = Ascii2Smw("You must finally  prove yourself    against the       apocalypse to     leave. Can you    beat us and use   the magic goal?   -Magikoopa Guild  ", 18 * 8 + 1)
				SubGame.SetMessageForLevel(Stage.Translevel.GetNumber(), 0, Message)
				Game.SetMessageForLevel(Stage.Translevel.GetNumber() + (SegmentNumber * 0x200), 0, Message)
				Message = Ascii2Smw("Welcome to the    Time Dimension!   Up ahead are threepipes. They each  represent morning,day, and night.   You must beat themall to leave here.", 18 * 8 + 1)
				SubGame.SetMessageForLevel(Stage.Translevel.GetNumber(), 1, Message)
				Game.SetMessageForLevel(Stage.Translevel.GetNumber() + (SegmentNumber * 0x200), 1, Message)
			# Set message 0 to 1 for this stage
			elif 'VLDC2-047' in Stage.Name:
				Message = Stage.SuperMarioWorld.GetMessageForLevel(Stage.Translevel.OriginalNumber, 0, Stage)
				SubGame.SetMessageForLevel(Stage.Translevel.GetNumber(), 1, Message)
				Game.SetMessageForLevel(Stage.Translevel.GetNumber() + (SegmentNumber * 0x200), 1, Message)
			else:
				# This level also uses the trick, but only for the two messages it'd natively have
				MessageBoxes = [True, True] if (('VLDC6-069' in Stage.Name) or ('VLDC4-SMWC Vanilla LDC 4 [#62]' in Stage.Name)) else Stage.HasMessageBoxes()
				for i in [0, 1]:
					if MessageBoxes[i]:
						Message = Stage.SuperMarioWorld.GetMessageForLevel(Stage.Translevel.OriginalNumber, i, Stage)
						SubGame.SetMessageForLevel(Stage.Translevel.GetNumber(), i, Message)
						Game.SetMessageForLevel(Stage.Translevel.GetNumber() + (SegmentNumber * 0x200), i, Message)

			Game.SetLevelName(Stage.Translevel.GetNumber() + (SegmentNumber * 0x200), Stage.GetStageName())
			Game.SetLevelAuthor(Stage.Translevel.GetNumber() + (SegmentNumber * 0x200), Stage.GetAuthorName())
			Game.SetContestNumber(Stage.Translevel.GetNumber() + (SegmentNumber * 0x200), Stage.GetContestNumber())
			Game.SetPiranhaFlags(Stage, SegmentNumber * 0x200)
			Game.SetSpritesPipesFlags(Stage, SegmentNumber * 0x200)
			TotalGoalCount += Game.SetStageExits(Stage, SegmentNumber * 0x200)

			SubGame.SetLevelName(Stage.Translevel.GetNumber(), Stage.GetStageName())
			SubGame.SetLevelAuthor(Stage.Translevel.GetNumber(), Stage.GetAuthorName())
			SubGame.SetContestNumber(Stage.Translevel.GetNumber(), Stage.GetContestNumber())
			SubGame.SetPiranhaFlags(Stage, SegmentNumber * 0x200)
			SubGame.SetSpritesPipesFlags(Stage, SegmentNumber * 0x200)
			SubGame.SetStageExits(Stage, 0)

			Authors.add(Stage.GetAuthorNameAscii())

		SubGame.Write()
		print('[compile.py]     Segment {} done!'.format(SegmentNumber))

	Game.InsertPaletteRows(PalCompress.GetPaletteRows())
	Game.FinalizeDemoReel()
	Game.PrepareRegistration()
	Game.Write()
	print('[compile.py]     SixPack done!')
	print('[compile.py]     Counted {} goals!'.format(TotalGoalCount))

	with open('credits.txt', 'w') as Credits:
		Formatted = set()
		Checker = set()

		for Author in Authors:
			if ' + ' in Author:
				for Single in Author.split(' + '):
					Single = Single.strip()
					if not Single.lower() in Checker:
						Formatted.add(Single)
						Checker.add(Single.lower())
			elif ' & ' in Author:
				for Single in Author.split(' & '):
					Single = Single.strip()
					if not Single.lower() in Checker:
						Formatted.add(Single)
						Checker.add(Single.lower())
			else:
				if not Author.lower() in Checker:
					Formatted.add(Author.strip())
					Checker.add(Author.lower())

		for Author in sorted(Formatted, key=str.casefold):
			Credits.write('{}\n'.format(Author))
	print('[compile.py]     Created credits.txt!')

def CompressPalettes(Stages):
	PalCompress = Palette()

	for Stage in Stages:
		for Level in Stage.Levels:
			PalCompress.Add(Level.GetPalette())
	
	for Stage in Stages:
		for Level in Stage.Levels:
			Level.SetCompressedPalette(PalCompress.Get(Level.GetPalette()))
	
	return PalCompress

def Register():
	Game = SuperMarioWorld(SixPackImageName)
	Game.Ruin()
	Game.Write()
	os.rename(SixPackImageName, 'SixPack.sfc')
	subprocess.call(['../{}'.format(PathToAssembler), '../asm/registration.asm', 'SixPack.sfc'])
	os.rename('SixPack.sfc', SixPackImageName)
	Game = SuperMarioWorld(SixPackImageName)
	Game.FixChecksum()
	Game.Write()
	print('[compile.py]      Checksum fixed!')

def WriteVerboseOutput(Stages):
	with open('log.txt', 'w') as Verbose:
		Verbose.write('SIX PACK by RAGEY built on {}\n'.format(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")))
		for Stage in Stages:
			Verbose.write('{}\n'.format(Stage.Verbose))

# Redirect program entry point.
if __name__ == '__main__':
	Main(sys.argv)
