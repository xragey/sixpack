################################################################################
#
# SIX PACK by Ragey
# fromsource.py
#
################################################################################

InputDirectory = 'input'

PathToLunarMagic = 'C:/Program Files (x86)/Lunar Magic/Lunar Magic.exe'
PathToPatcher = 'bin/flips.exe'
PathToRecovery = 'bin/mrlm.exe'
Original = 'base/SuperMarioWorld.smc'

################################################################################

import shutil
import subprocess
import sys
import os

################################################################################

def Main(Arguments):
	ClearInputDirectory()
	Extract()

def ClearInputDirectory():
	shutil.rmtree('{}/gfx'.format(InputDirectory), ignore_errors = True)
	os.mkdir('{}/gfx'.format(InputDirectory))
	shutil.rmtree('{}/map16'.format(InputDirectory), ignore_errors = True)
	os.mkdir('{}/map16'.format(InputDirectory))
	shutil.rmtree('{}/mwl'.format(InputDirectory), ignore_errors = True)
	os.mkdir('{}/mwl'.format(InputDirectory))
	shutil.rmtree('{}/rom'.format(InputDirectory), ignore_errors = True)
	os.mkdir('{}/rom'.format(InputDirectory))

def Extract():
	for i in [1, 2, 3, 4, 5, 6]:
		for Name in os.listdir('{}/patch/{}/'.format(InputDirectory, i)):
			Out = ('VLDC{}-'.format(i) + Name[:-4]).replace('.', '_')
			OutName = Out + '.smc'
			OutPath = '{}/rom/{}'.format(InputDirectory, OutName)
			subprocess.call([PathToPatcher, '--apply', '{}/patch/{}/{}'.format(InputDirectory, i, Name), Original, OutPath])
			subprocess.call([PathToRecovery, OutPath, OutPath])
			subprocess.call([PathToLunarMagic, '-ExportMultLevels', OutPath, '{}/mwl/{}'.format(InputDirectory, Out)])
			subprocess.call([PathToLunarMagic, '-ExportExGFX', OutPath])
			shutil.move('ExGraphics', '{}/gfx/{}/'.format(InputDirectory, Out))
			subprocess.call([PathToLunarMagic, '-ExportGFX', OutPath])
			shutil.move('Graphics', '{}/gfx/{}/Graphics/'.format(InputDirectory, Out))
			subprocess.call([PathToLunarMagic, '-ExportAllMap16', OutPath, '{}/map16/{}.map16'.format(InputDirectory, Out)])

# Redirect program entry point.
if __name__ == '__main__':
	Main(sys.argv)
