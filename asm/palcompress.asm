;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; SIX PACK by Ragey
; palcompress.asm
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

incsrc "_common.asm"
fullsa1rom

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

org $0EF5B8
	jmp DecompressPalette

org !cCodeDecompressPalette
DecompressPalette:
	rep #$10
	tyx

-	lda [$04],y
	bpl +
	
	; Column row reference
	jsr DecompressPaletteRow
	bra ++

+	; Direct color
	sta $6703,x

	; Loop iterator
	inx #2
++	iny #2
	cpx #$0201
	bcc -

	sep #$10
	rts

DecompressPaletteRow:
	phy
	txy
	asl #5
	tax
	lda.l !cPaletteData+$0,x
	sta $6703+$0,y
	lda.l !cPaletteData+$2,x
	sta $6703+$2,y
	lda.l !cPaletteData+$4,x
	sta $6703+$4,y
	lda.l !cPaletteData+$6,x
	sta $6703+$6,y
	lda.l !cPaletteData+$8,x
	sta $6703+$8,y
	lda.l !cPaletteData+$A,x
	sta $6703+$A,y
	lda.l !cPaletteData+$C,x
	sta $6703+$C,y
	lda.l !cPaletteData+$E,x
	sta $6703+$E,y
	lda.l !cPaletteData+$10,x
	sta $6703+$10,y
	lda.l !cPaletteData+$12,x
	sta $6703+$12,y
	lda.l !cPaletteData+$14,x
	sta $6703+$14,y
	lda.l !cPaletteData+$16,x
	sta $6703+$16,y
	lda.l !cPaletteData+$18,x
	sta $6703+$18,y
	lda.l !cPaletteData+$1A,x
	sta $6703+$1A,y
	lda.l !cPaletteData+$1C,x
	sta $6703+$1C,y
	lda.l !cPaletteData+$1E,x
	sta $6703+$1E,y
	tya
	clc
	adc #$0020
	tax
	ply
	rts
	warnpc !cCodeDecompressPaletteEnd
