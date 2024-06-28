;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; SIX PACK by Ragey
; warning.asm
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

incsrc "_common.asm"
fullsa1rom

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

org $009369
	dw FadeIn
	dw DisplayWarning

org $0096AE
	jsr SplitGameMode

org !cCodeWarning
SplitGameMode:
	lda !Warning
	bne +
	inc a
	sta !Warning
	lda #$20
	sta $6100
	sta $73D2
	lda #$4B
	sta $7DF5
	pla
	pla
	rts
+	stz $4200
	rts

FadeIn:
	lda #$20
	sta $40
	lda #$12
	sta $44
	lda #$02
	sta $7426
	stz $73BF
	stz !Segment
	jsl $7F8000
	jsl $05B10C
	lda $7B89
	cmp #$50
	bcc +
	jmp $9F6F
+	rts

DisplayWarning:
	jsl $05B10C
	lda $7DF5
	bne +
	lda #$02
	sta $6100
+	rts
	warnpc !cCodeWarningEnd
