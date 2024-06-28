;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; SIX PACK by Ragey
; owdisplay.asm
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

incsrc "_common.asm"
fullsa1rom

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

org !cDataContestNumbers
	rep 768 : db $1F

org !cDataAuthorNames
	rep $4500 : db $1F

org !cDataStageNames
	rep $3900 : db $1F

org !cDataPointerOffsets
ContestOffsetsPerSegment:
	dw $0000,$0060,$00C0,$0120,$0180,$01E0,$0240,$02A0
TranslevelNamesOffsetsPerSegment:
	dw $0000,$0720,$0E40,$1560,$1C80,$23A0,$2AC0,$31E0
AuthorOffsetsPerSegment:
	dw $0000,$08A0,$1140,$19E0,$2280,$2B20,$33C0,$3C60
warnpc !cDataPointerOffsetsEnd

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; When writing the overworld tile type, also write the segment offset.
org $049384
	jsr SetSegment

org $04A1B6
TileToSegment:
	db                         $00,$00,$00,$00,$00,$00,$00,$00,$00,$00	; 56-5F
	db $00,$00,$00,$02,$04,$06,$08,$0A,$0C,$0E,$00,$02,$04,$06,$00,$00	; 60-6F
	db $00,$00,$08,$0A,$0C,$0E                                          ; 70-75

SetSegment:
	tax
	lda.l TileToSegment-$56,x
	and #$00FF
	sta !Segment
	txa
	sta $73C1
	rts
warnpc $04A400

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; Apparently the logic is slightly different (and also ordered differently) in
; two player mode, which messes up the border names. This code fixes this.

org $048E78
	ldx $04
	bmi +
	cpx #$0800
	bcs +
	lda.l $40C800,x
	and #$00FF
	jsr SetSegment
+	ldx $04
	lda.l $40D000,x
	and #$00FF
	jsl $03BB20
	nop #6
	warnpc $048E9E

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; Disable drawing lives to the overworld display and draw the VLDC# instead.
org $05DBF2
	rtl

DrawContestNumber:
	rep #$20
	ldx $04
	lda $40D000,x
	and #$00FF
	sta $02
	jsl ContestNumberIndex
	clc
	adc #$0004
	sta $837B
	lda #$0100
	sta $837F,y
	lda #$8850
	sta $837D,y
	sep #$20
-	lda.l !cDataContestNumbers,x
	sta $8381,y
	lda #$39
	sta $8382,y
	iny #2
	inx
	cpy $02
	bcc -
	lda #$FF
	sta $8381,y
	rtl
	warnpc $05DC39

org $03BB2E
	jsr StageNameIndex

org $03BB56
	lda.l !cDataStageNames,x

org !cCodeStageNameIndex
StageNameIndex:
	adc $00
	sep #$10
	ldx !Segment
	clc
	adc.l TranslevelNamesOffsetsPerSegment,x
	rep #$10
	tax
	rts

ContestNumberIndex:
	sep #$10
	pha
	lda.l !Segment
	tax
	pla
	clc
	adc.l ContestOffsetsPerSegment,x
	rep #$10
	tax
	lda $837B
	tay
	clc
	adc #$0002
	sta $02
	rtl
warnpc !cCodeStageNameIndexEnd

; Modified Lunar Magic routine. Hijack the end to expand the routine.
org $03BB6E
DrawStageName:
	rep #$20
	ldx $04
	lda $40d000,x
	and #$00FF
	sta $02
	sta !OverworldIndex
	asl #3			; x8
	sta $00
	asl				; x16
	clc
	adc $00			; x24
	sec
	sbc $02			; x23
	jmp DrawAuthorName
	warnpc $03BB90

; Draw author name to the overworld display.
org !cCodeDrawAuthorName
DrawAuthorName:
	sep #$10
	pha
	lda.l !Segment
	tax
	pla
	clc
	adc.l AuthorOffsetsPerSegment,x
	rep #$10
	tax
	lda $837B
	tay
	clc
	adc #$002E
	sta $02
	clc
	adc #$0004
	sta $837B
	lda #$2D00
	sta $837F,y
	lda #$4750
	sta $837D,y
	sep #$20
-	lda.l !cDataAuthorNames,x
	sta $8381,y
	lda #$39
	sta $8382,y
	iny #2
	inx
	cpy $02
	bcc -
	lda #$FF
	sta $8381,y
	jsl DrawContestNumber

	rep #$20
	plb
	rtl
	warnpc !cCodeDrawAuthorNameEnd