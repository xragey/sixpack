;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; SIX PACK by Ragey
; messages.asm
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

incsrc "_common.asm"
fullsa1rom

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

org $03BBC9
	jsr GetMessageIndirectIndex

org $03BBD6
	lda.l !cDataMessagePointers,x
	nop

org $03BC0A
	lda.l !cDataMessages,x

org !cCodeMessages
GetMessageIndirectIndex:
	rep #$30
	txa
	ldx !Segment
	clc
	adc.l !cDataPointerOffsets,x
	rts
	warnpc !cCodeMessagesEnd

; Do not change message logic for Yoshi message specifically. This is needed
; to fix a specific contest entry, and Yoshi messages are disabled anyway.
org $03BB95
	nop #2

; Do not move Mario's overworld position on closing message from sprite 0x19.
org $01E762
	nop #6

org $05B15D
	nop #3
