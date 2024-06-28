;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; SIX PACK by Ragey
; dragoncoin.asm
;
; Uses the midway logic for ram and to clear flags.
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

incsrc "_common.asm"
fullsa1rom

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; Check if Checkpoints collected
org $0DA5A7
	nop #2
	jsr GetOffsetBank0D
	and #$08

; Check if 3UP moon collected
org $0DA59C
	nop #2
	jsr GetOffsetBank0D
	and #$04

; Check if Dragon Coins collected
org $0DB2D7
	nop #2
	jsr GetOffsetBank0D
	and #$02

org !cCodeCheckObjectBank0D
GetOffsetBank0D:
	rep #$30
	lda !Segment
	and #$000E
	tax
	lda $73BF
	clc
	adc.l !cDataPointerOffsets,x
	tax
	lda.l !Midway,x
	sep #$30
	rts
warnpc !cCodeCheckObjectBank0DEnd

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

org $00F2B5
	nop
	php
	jsr GetOffsetBank00
	jsr SetCheckPoint
	plp

org $00F31F
	nop
	php
	jsr GetOffsetBank00
	jsr Set3UpMoon
	plp

org $00F34E
	nop
	php
	jsr GetOffsetBank00
	jsr SetDragonCoin
	plp

org !cCodeCheckObjectBank00
GetOffsetBank00:
	rep #$30
	lda !Segment
	and #$000E
	tax
	lda $73BF
	clc
	adc.l !cDataPointerOffsets,x
	tax
	lda.l !Midway,x
	rts

SetCheckPoint:
	ora #$0008
	sta.l !Midway,x
	rts

Set3UpMoon:
	ora #$0004
	sta.l !Midway,x
	rts

SetDragonCoin:
	ora #$0002
	sta.l !Midway,x
	rts
warnpc !cCodeCheckObjectBank00End
