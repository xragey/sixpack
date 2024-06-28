;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; SIX PACK by Ragey
; remap16.asm
;
; Implements extended object 0x4 which remaps tiles in a level with a different
; tile. This is needed to handle user-made changes to tiles on pages 0 and/or 1,
; which may then be called by vanilla objects. Note that this is not needed for
; Lunar Magic's "Direct Map16" objects, which are remapped at assembly instead.
;
; The remap is also applied to tiles generated with $00BEB0.
;
; Extended object 0x4 format:
;   000WWWWW 0000wwww 00000100 11111111 [mmmmmmmm MNNNNNNN nnnnnnnn ...]
;   * Mm (0-0x1FF) is the tile number to replace with Nn (0-0x7FFF).
;   * The last set of three bytes repeats Ww+1 times.
;   * The fourth byte is $FF (for Lunar Magic to render the level properly).
;   * Extended object 0x4 must be the very last object.
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

incsrc "_common.asm"
fullsa1rom

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

org $0DA11B
	dl ExtendedObject04

org !cCodeRemap16
ExtendedObject04:
	; Prologue, set object pointer 3 slots back to read command length
	rep #$30
	lda $65
	pha
	sec
	sbc #$0003
	sta $65
	ldy #$0000

	; Clear table
	ldx #$01FE
	lda #$FFFF
-	sta !Map16RemapTableHigh,x
	dex
	dex
	bpl -

	; $00 = Amount of replacements
	lda [$65],y
	xba
	and #$000F
	sta $00
	lda [$65],y
	and #$001F
	asl #4
	ora $00
	sta $00

	ldy #$0004
	
-	; X = Source tile (000-1FF)
	clc
	lda [$65],y
	and #$00FF
	sta $02
	lda [$65],y
	and #$8000
	rol #2
	sta $03
	ldx $02

	; Put replacement tile in table (200-7FFF)
	iny
	lda [$65],y
	xba
	and #$7FFF
	sep #$20
	sta.l !Map16RemapTableLow,x
	xba
	sta !Map16RemapTableHigh,x
	jsr CheckTileGen
	rep #$20
	iny #2
	dec $00
	bpl -

	; Perform tile replacement
	pla
	sta $65
	lda #$0000
	sep #$20
	ldx #$37FF

-	lda.l $41C800,x
	cmp #$02
	bcs +
	xba
	lda.l $40C800,x
	tay
	lda !Map16RemapTableHigh,y
	bmi +
	sta $41C800,x
	stx $00
	tyx
	lda.l !Map16RemapTableLow,x
	ldx $00
	sta $40C800,x
+	dex
	bpl -

	sep #$10
	rts

CheckTileGen:
	macro CheckTile(Tile, Page, Offset)
		cpx.w #<Tile>
		bne ?+
		sta.l !TileGen<Page>High+<Offset>
		xba
		sta.l !TileGen<Page>Low+<Offset>
		rts
	?+
	endmacro

	cpx #$0025
	bne +
	sta.l !TileGen0High+0
	sta.l !TileGen0High+1
	sta.l !TileGen0High+2
	xba
	sta.l !TileGen0Low+0
	sta.l !TileGen0Low+1
	sta.l !TileGen0Low+2
	rts
+	%CheckTile($0006, 0, 3)
	%CheckTile($0049, 0, 4)
	%CheckTile($0048, 0, 5)
	%CheckTile($002B, 0, 6)
	%CheckTile($00A2, 0, 7)
	%CheckTile($00C6, 0, 8)
	%CheckTile($0152, 1, 0)
	%CheckTile($011B, 1, 1)
	%CheckTile($0123, 1, 2)
	%CheckTile($011E, 1, 3)
	cpx #$0132
	bne +
	sta.l !TileGen1High+4
	sta.l !TileGen1High+13
	xba
	sta.l !TileGen1Low+4
	sta.l !TileGen1Low+13
	rts
+	%CheckTile($0113, 1, 5)
	%CheckTile($0115, 1, 6)
	%CheckTile($0116, 1, 7)
	%CheckTile($012B, 1, 8)
	%CheckTile($012C, 1, 9)
	%CheckTile($0112, 1, 10)
	%CheckTile($0168, 1, 11)
	%CheckTile($0169, 1, 12)
	%CheckTile($015E, 1, 14)
	cpx #$0045
	bne +
	sta.l !TileBerries+1
	xba
	sta.l !TileBerries
+	cpx #$0046
	bne +
	sta.l !TileBerries+3
	xba
	sta.l !TileBerries+2
+	cpx #$0047
	bne +
	sta.l !TileBerries+5
	xba
	sta.l !TileBerries+4	
+	rts
	warnpc !cCodeRemap16End
