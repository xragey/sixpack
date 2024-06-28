;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; SIX PACK by Ragey
; gfx33.asm
;
; Implements translevel-specific GFX33 support for those few levels that changed
; this file.
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

incsrc "_common.asm"
fullsa1rom

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

org !cCodeGfx33Handler
LoadGFX33:
	; Never reload GFX33 if this is not a translevel.
	lda $741A
	and #$00FF
	bne ++

	; Check if this is one of the levels that has a changed GFX33.
	phb
	phk
	plb

	lda $0E
	ldx #$0000
-	cmp.l !cDataGfx33Users,x
	beq +
	inx
	inx
	cpx.w #(!cCountStagesWithGFX33Altered<<1)
	bne -

	; Restore standard GFX33
	php
	sep #$30
	jsr $B888
	plp
	plb
++	rtl

+	; Convert ExGFX number to pointer
	lda.l !cDataGfx33Identifiers,x
	sec
	sbc #$0080
	sta $00
	asl
	clc
	adc $00
	tax

	; Call GFX32 decompressor with altered pointer for GFX33
	lda.l $0FF600,x
	sta $8A
	php
	sep #$20
	lda.l $0FF602,x
	sta $8C
	jsr $B893
	plp
	plb
	rtl

FixGFX33:
	sta $8A
	sep #$20
	lda #$08
	sta $8C
	rts
	warnpc !cCodeGfx33HandlerEnd

; Fix pointer back for GFX32, which seems to be hardcoded by Lunar Magic to use bank $08.
org $00B8DA
	jsr FixGFX33
	nop
