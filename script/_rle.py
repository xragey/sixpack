###############################################################################
#
# SIX PACK by Ragey <i@ragey.net>
# _rle.py
#
# Run-length encoding as used by Super Mario World for background images. Note
# that this implementation is incomplete, it lacks some possible optimisations.
# But it does produce correct output, which is good enough for this project.
#
###############################################################################

import struct

###############################################################################

def RLE1(Binary):
	Output = bytearray()
	Current = None
	Length = 0
	Sequence = []

	for Byte in Binary:
		# Character changes
		if Length > 0 and Byte != Current:
			if len(Sequence) == 0:
				Output.append((Length - 1) | 0x80)
				Output.append(Current)
				Length = 1
			if len(Sequence) == 128:
				Output.append(len(Sequence) - 1)
				Output.extend(Sequence)
				Sequence = []
			else:
				Sequence.append(Byte)
			Current = Byte
		
		# Character stays the same...
		elif Length > 0:
			if len(Sequence) == 1:
				Sequence = []
			if len(Sequence) > 1:
				Sequence.pop()
				Output.append(len(Sequence) - 1)
				Output.extend(Sequence)
				Sequence = []
	
			if Length < 128:
				Length += 1
			else:
				Output.append((Length - 1) | 0x80)
				Output.append(Current)
				Length = 1
				Current = Byte
		
		# Handle first character in stream
		else:
			Length = 1
			Current = Byte
	
	if len(Sequence) > 0:
		Output.append(len(Sequence) - 1)
		Output.extend(Sequence)
	elif Length > 0:
		Output.append((Length - 1) | 0x80)
		Output.append(Current)

	Output.extend([0xff, 0xff])
	return Output
