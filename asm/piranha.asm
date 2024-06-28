;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; SIX PACK by Ragey
; piranha.asm
;
; Implements the Piranha Fix patch, which was for some reason allowed for the
; vanilla contests. In addition, two entries changed the property byte. This
; patch takes care of switching among them.
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

incsrc "_common.asm"
fullsa1rom

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

org $018E8A
	jsl PiranhaPropertyByte
	nop #9

org !cCodePiranhaPropertyByte
PiranhaPropertyByte:
	; Check if this level uses the patch
	phx
	ldx !Segment
	rep #$30
	lda $73BF
	and #$00FF
	clc
	adc.l !cDataPointerOffsets,x
	tax
	lda.l !cDataDemoReel,x
	sep #$30
	plx
	and #$20
	beq .NoPatch

	; Patch is installed
	ldy #$0A
	lda !Segment
	xba
	lda $73BF
	rep #$20
	cmp #$0406
	beq +
	cmp #$080C
	beq +
	ldy #$0B
+	sty $79
	sep #$20
	ldy $33A2,x
	lda $3200,x
	cmp #$2A
	bne +
	iny #4
+	lda $6307,y
	and #$F1
	ora $79
	sta $6307,y
	rtl

.NoPatch
	ldy $33A2,x
	lda $630B,y
	and #$F1
	ora #$0B
	sta $630B,y
	rtl
	warnpc !cCodePiranhaPropertyByteEnd