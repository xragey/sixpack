;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; SIX PACK by Ragey
; pswitch.asm
;
; Some levels fix the sprites-through-pipe glitch.
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

incsrc "_common.asm"
fullsa1rom

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

org $02AC16
	jmp ConditionalPSwitchBranch
	nop

org !cCodeSpriteThruPipes
ConditionalPSwitchBranch:
	; Check if this level uses the patch
	php
	ldx !Segment
	rep #$30
	lda $73BF
	and #$00FF
	clc
	adc.l !cDataPointerOffsets,x
	tax
	lda.l !cDataDemoReel,x
	sep #$30
	and #$10
	beq .NoPatch

.PatchApplied
	plp
	ldx $00
-	jmp $AC48

.NoPatch
	plp
	ldx $00
	bmi -
	jmp $AC1A
warnpc !cCodeSpriteThruPipesEnd

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

org $01A21D
	jsr UpdateSwitchColour

org !cCodePSwitchColour
UpdateSwitchColour:
	ldy $3284,x
	lda $33B8,x
	and #$F1
	ora $8466,y
	sta $33B8,x
	jmp $9F0D
	warnpc !cCodePSwitchColourEnd
