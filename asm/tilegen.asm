;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; SIX PACK by Ragey
; tilegen.asm
;
; Changes the tile generation routine ($00BEB0) to create tiles based on a table
; in RAM. This is needed for tiles that change tiles on one of the first two
; pages of Map16. Also changes the berry tiles Yoshi can eat in a similar way.
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

incsrc "_common.asm"
fullsa1rom

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; Initialize the table with SMW defaults, later the remap16.asm object may
; change the contents of the table.

org $0583B2
	jsr InitializeTileGen

org !cCodeTileGen
InitializeTileGen:
	ldx #$0E
-	lda.l $00C06B,x
	sta.l !TileGen0Low,x
	lda #$00
	sta.l !TileGen0High,x
	lda.l $00C0B2,x
	sta.l !TileGen1Low,x
	lda #$01
	sta.l !TileGen1High,x
	dex
	bpl -
	rep #$20
	lda #$0045
	sta !TileBerries
	lda #$0046
	sta !TileBerries+2
	lda #$0047
	sta !TileBerries+4
	sep #$20
	jmp $84E3

Write0025LowAndHigh:
	lda.l !TileGen0High
	sta [$6E],y
	xba
	lda.l !TileGen0Low
	sta [$6B],y
	rtl
	warnpc !cCodeTileGenEnd

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; Handle tile changes via the $00BEB0 function.

org $00C094
TileGenLow:
	lda.l !TileGen0High,x
	sta [$6E],y
	xba
	lda.l !TileGen0Low,x
	sta [$6B],y
	bra +
	warnpc $00C0AA

org $00C0E5
TileGenHigh:
	lda.l !TileGen1High,x
	sta [$6E],y
	xba
	lda.l !TileGen1Low,x
	sta [$6B],y
	nop #5
+	rep #$20
	asl
	tay
	warnpc $00C0FB

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; Handle Yoshi attempting to eat a Berry.

org $02BA92
	ldx $75E9
	lda #$41
	sta $07
	lda [$05]
	xba
	dec $07
	lda [$05]
	sta $7693
	jsr CheckBerry 
	nop #7
	warnpc $02BAAD

org $02D1AD
	ldx $75E9
	lda #$41
	sta $07
	lda [$05]
	xba
	dec $07
	lda [$05]
	sta $7693
	jsr CheckBerry 
	nop #7
	warnpc $02D1C8

org $02B9FE
CheckBerry:
	rep #$20
	ldy #$45
	cmp !TileBerries
	beq +
	ldy #$46
	cmp !TileBerries+2
	beq +
	ldy #$47
	cmp !TileBerries+4
	beq +
	sep #$20
	sec
	rts
+	sep #$20
	tya
	clc
	rts
	warnpc $02BA46

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; Handle collecting a Yoshi Coin or pressing a Switch Palace switch. The vanilla
; code does not respect changes to map16 high for these instances.

org $00C1C6 : jsl Write0025LowAndHigh
org $00C1D4 : jsl Write0025LowAndHigh
org $00C1DA : nop #3
org $00C3ED : jsl Write0025LowAndHigh
org $00C3F2 : jsl Write0025LowAndHigh
org $00C400 : jsl Write0025LowAndHigh
org $00C405 : jsl Write0025LowAndHigh
