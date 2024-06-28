;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; SIX PACK by Ragey
; mariopalette.asm
;
; Changes the engine to allow for per-level Mario palettes. The overworld and
; levels will, by default, load the set with index 0. Levels may overwrite this
; by inserting extended object 0x6.
;
; Extended object 0x6 format:
;   000ppppp 0000-PP- 00000110
;   * Pp (0-0x7F) is the palette index to use.
;   * - is unused/for future use.
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

incsrc "_common.asm"
fullsa1rom

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

org $0DA121
	dl ExtendedObject06

org !cCodeMarioPaletteObject
ExtendedObject06:
	lda $65
	pha
	sec
	sbc #$03
	sta $65
	ldy #$01
	lda [$65],y
	and #$06
	asl #4
	dey
	ora [$65],y
	rep #$30
	jsl SetMarioLuigiPalette
	sep #$30
	pla
	sta $65
	rts
	warnpc !cCodeMarioPaletteObjectEnd

org $00B2C8
; Assumes axy16. Load in lower A the index to load.
; Call this function during:
; - translevel load (done in pointer.asm)
; - overworld load (done in owpalette.asm)
SetDefaultMarioLuigiPalette:
	lda #$0000

SetMarioLuigiPalette:
	and #$007F
	asl #4
	sta $00
	asl #2
	clc
	adc $00
	sta $00
	ldx #$000E
-	lda.l MLPalettePointers,x
	clc
	adc $00
	sta !MarioLuigiPalettePtr,x
	dex
	dex
	bpl -
	rtl
	warnpc $00B318

org $00E2A2
MLPalettePointers: ; Starting with the default ones (16 bytes each)
	dw MLPaletteData,MLPaletteData+20,MLPaletteData,MLPaletteData+20
	dw MLPaletteData,MLPaletteData+20,MLPaletteData+40,MLPaletteData+60

org !cDataMarioLuigiPalette
MLPaletteData: ; Starting with the default ones (80 bytes each)
	dw $635F,$581D,$000A,$391F
	dw $44C4,$4E08,$6770,$30B6
	dw $35DF,$03FF
	dw $4F3F,$581D,$1140,$3FE0
	dw $3C07,$7CAE,$7DB3,$2F00
	dw $165F,$03FF
	dw $635F,$581D,$2529,$7FFF
	dw $0008,$0017,$001F,$577B
	dw $0DDF,$03FF
	dw $3B1F,$581D,$2529,$7FFF
	dw $1140,$01E0,$02E0,$577B
	dw $0DDF,$03FF

; Change upload routine to always upload from bank $0E (instead of $00).
org $00A31A
	ldy.b #(MLPaletteData>>16)

; Change palette pointer seek to always load pointers from RAM instead of ROM.
org $00E31E
	lda.w !MarioLuigiPalettePtr,y

