;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; SIX PACK by Ragey
; pointer.asm
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

incsrc "_common.asm"
fullsa1rom

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

org $03BCED
	jsr SecondaryEntranceApplySegmentHighBits

org $03BA02
SecondaryEntranceApplySegmentHighBits:
	lsr #3
	ora !Segment
	rts
	warnpc $03BA10

; When entering a level other than the translevel
org $05D7C0
	sta $0E
	lda $6DD6
	lsr #2
	tay
	lda $7F11,y
	jsl $05DC50
	jsr ApplySegmentHighBits
	sta $0F
	warnpc $05D7D4

; Fix jump offset (secondary entrance)
org $05D83B
	jmp LoadLevel

; When entering a translevel for the first time
; Set $0E to the absolute stage number (it can be higher than $01FF now).
; Remap layer 1 and layer 2 pointers.
org $05D8A2
LoadStage:
	cmp #$25
	bcc +
	sec
	sbc #$24
+	sta $0E
	lda $7F11,y
	jsl $05DCD0			; Lunar Magic
	ora !Segment
	sta $0F
LoadLevel:
	rep #$30
	nop #4
	jsl !cCodeGfx33Handler
	lda $0E
	pha
	asl
	clc
	adc $0E
	tax
	lda.l !cDataLayer1Pointers,x
	sta $65
	lda.l !cDataLayer1Pointers+1,x
	sta $66
	lda.l !cDataLayer2Pointers,x
	sta $68
	lda.l !cDataLayer2Pointers+1,x
	sta $69
	nop #1
	warnpc $05D8E2 : skip 4
	tax
	lda.l !cDataSpritePointers,x
	sta $CE
	lda #$0000
	sep #$20
	plx
	lda.l !cDataSpriteBankPointers,x
	sta $D0
	warnpc $05D8F9

; Remap secondary stage header tables.
org $05D907
	sep #$20
	ldx $0E
	lda.l !cDataStageHeader05F000,x
	lsr
	lsr
	lsr
	lsr
	tay
	lda.w $05D720,y
	sta $7413
	lda.w $05D710,y
	sta $7414
	lda.b #$01
	sta $7411
	lda.l !cDataStageHeader05F200,x
	and #$C0
	clc
	asl
	rol
	rol
	sta $7BE3
	stz $1D
	stz $21
	lda.l !cDataStageHeader05F600,x
	and #$80
	jsr StoreNoYoshiEntranceFlag
	lda.l !cDataStageHeader05F600,x
	and #$60
	lsr
	lsr
	lsr
	lsr
	lsr
	sta $5B
	lda $7B93
	bne +
	lda.l !cDataStageHeader05F000,x
	and #$0F
	tay
	lda.w $05D730,y
	sta $96
	lda.w $05D740,y
	sta $97
	lda.l !cDataStageHeader05F200,x
	sta $02
	and #$07
	tay
	lda.w $05D750,y
	sta $94
	lda.w $05D758,y
	sta $95
	lda $02
	and #$38
	lsr
	lsr
	nop #2
	warnpc $05D97D : skip 4
	ldx $0E
	lda.l !cDataStageHeader05F400,x
	sta $02
	and #$03
	tay
	lda.w $05D70C,y
	sta $20
	lda $02
	and #$0C
	lsr
	lsr
	tay
	lda.w $05D708,y
	jsr CopyStageHeader05F600ToScratch01
+	nop #3
	warnpc $05D9A1

; Remap secondary stage header tables introduced by Lunar Magic.
org read3($05D97E)
	lsr
	sta $792A
;	tyx
	lda.l !cDataStageHeader06FC00,x
	sta $04
	lda.l !cDataStageHeader06FE00,x
	sta $73CD
	lda.l !cDataStageHeader05DE00,x
	tay
	and #$C0
	tsb $792A
	tya
	bit #$20
	beq +
	and #$18
	asl #4
	sta $94
	rol
	sta $95
	lda.l !cDataStageHeader05F200,x
	asl #4
	and #$70
	tsb $94
	lda.l !cDataStageHeader05F000,x
	asl #4
	sta $96
	lda $04
	and #$3F
	sta $97
+	rtl
	warnpc $05DD7B

; Remap another secondary stage header table introduced by Lunar Magic.
; These seem to be part of the secondary entrance handler
org $03BD0F
	lda.l !cDataStageHeader06FC00,x

org $03BD17
	lda.l !cDataStageHeader06FE00,x

; Remap another secondary stage header table introduced by Lunar Magic.
org read3($05D9A2)
	skip 76
	lda.l !cDataStageHeader05DE00,x

; Remap another secondary stage header table.
org $0EF51F
	lda.l !cDataStageHeader0EF310,x

; Remap Lunar Magic custom palette pointers.
org $0EF588
	rep #$11
	sta $00
	asl
	adc $00
	tax
	lda.l !cDataPalettePointers,x
	sta $04
	lda.l !cDataPalettePointers+1,x
	warnpc $0EF59A

; Remap Lunar Magic ExAnimation settings data table.
org read3($0583AE)
	skip 69
	lda.l !cDataStageHeader03FE00,x
	skip 149
	lda.l !cDataStageExAnimPointers+1,x
	skip 7
	lda.l !cDataStageExAnimPointers,x

; Remap graphics override data table.
org $0FF7FE
	jsl GetGraphicsBypassPointer
	pha
	txa
	sta.l $7FC006
	sep #$20
	lda.b #(!cDataGraphicsBypass0>>16)
	adc #$00
	sta.l $7FC008
	nop #2
	warnpc $0FF814

; Fix certain "No Yoshi" level sprite data pointer, which no longer exists in its original position.
; This needs the data for "no sprites", a.k.a. "$00 $FF", which exists at $0192C7.
org $05DA7E
	lda #$C7
	sta $CE
	lda #$92
	sta $CF
	lda #$01
	sta $D0

org !cCodePointerLogicBank05
ApplySegmentHighBits:
	ldx $7B93
	bne +
	ora !Segment
+	rts

CopyStageHeader05F600ToScratch01:
	sta $1C
	lda.l !cDataStageHeader05F600,x
	sta $01
	rts

GetGraphicsBypassPointer:
	bcs +
	lda.l !cDataGraphicsBypass0,x
	rtl
+	lda.l !cDataGraphicsBypass4,x
	rtl

; For the random level on the title screen.
StoreNoYoshiEntranceFlag:
	sta $741F
	lda $6100
	cmp #$0B
	bcs +
	lda #$80
	sta $741F
+	rts
warnpc !cCodePointerLogicBank05End