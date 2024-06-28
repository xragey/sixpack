;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; SIX PACK by Ragey
; owprogress.asm
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

incsrc "_common.asm"

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

org $049132
	jsl DrawOverworldProgress

org !cCodeOverworldProgress
DrawOverworldProgress:
	; Compute draw position
	ldx #$0C
	stx $6DDE
	ldy $6DD6
	lda $7F17,y
	sec
	sbc #$08
	sta $6E35,x
	lda $7F18,y
	sbc #$00
	sta $6E65,x
	lda $7F19,y
	sec
	sbc #$1E
	sta $6E45,x
	lda $7F1A,y
	sbc #$00
	sta $6E75,x
	stz $6E55,x
	stz $6E85,x
	jsr $FE62

	; Get amount of exits for this stage
	ldy #$00
	ldx !Segment
	rep #$30
	lda !OverworldIndex
	and #$00FF
	clc
	adc.l !cDataPointerOffsets,x
	tax
	phx
	sep #$20
	lda.l !cDataDemoReel,x
	and #$C0
	sta $08
	bne +
	jmp .OverwriteTiles
+	cmp #$C0
	bne +
	iny
+	sep #$10
	phy

	; Draw text balloon
	ldx .Size,y
	ldy #$10
-	lda $00
	clc
	adc .XOffset,x
	sta $6308,y
	lda $02
	clc
	adc .YOffset,x
	sta $6309,y
	lda .Tile,x
	sta $630A,y
	lda .Properties,x
	sta $630B,y
	dex
	dey #4
	bpl -

	; Draw balloon contents
	ldy #$04
	plx
	cpx #$00
	beq .DrawSingle

.DrawDouble
-	lda $00
	clc
	adc .ContentXOffset,x
	sta $6300,y
	lda $02
	clc
	adc #$F4
	sta $6301,y
	lda .ContentTile,x
	sta $6302,y
	lda #$32
	sta $6303,y
	dey #4
	dex
	bpl -
	bra .SetTileSizes

.DrawSingle
	lda $00
	sta $6300
	lda $02
	clc
	adc #$F4
	sta $6301
	lda #$48
	sta $6302
	lda #$32
	sta $6303

.SetTileSizes
	lda #$02
	sta $6460
	sta $6461
	sta $6462
	sta $6463
	sta $6464
	sta $6465
	sta $6466

.OverwriteTiles
	rep #$10
	plx
	lda.l !PersistentExitFlags,x
	sep #$10
	ldx $610A
	bit .Normal,x
	beq +
	ldy #$68
	sty $6302
+	bit .Secret,x
	beq +
	ldy #$68
	lda $08
	cmp #$40
	bne ++
	sty $6302
++	sty $6306
+	rtl

.XOffset
	db $00,$FC,$03,$FC,$03
	db $00,$F8,$07,$F8,$07
.YOffset
	db $00,$F0,$F0,$F8,$F8
	db $00,$F0,$F0,$F8,$F8
.Properties
	db $32,$32,$72,$B2,$F2
	db $32,$32,$72,$B2,$F2
.Tile
	db $26,$4C,$4C,$4C,$4C
	db $26,$4C,$4C,$4C,$4C
.Size
	db $04,$09
.ContentXOffset
	db $FA,$05
.ContentTile
	db $48,$4A
.Flags
	db $03,$0C,$30,$C0
.Normal
	db $01,$04,$10,$40
.Secret
	db $02,$08,$20,$80
warnpc !cCodeOverworldProgressEnd