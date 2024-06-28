;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; SIX PACK by Ragey
; midway.asm
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

incsrc "_common.asm"
fullsa1rom

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; On initial load, clear the midway ram flags
org $0096B1
	jsr ClearMidwayFlags_Initial

; On level exited (copy midway flag to persistent RAM)
org $048F43
	ldx $04
	lda.l $40D000,x
	and #$00FF
	ldx !Segment
	clc
	jsl SetMidwayFlag
	nop #2
	warnpc $048F56

; On level beaten (clear midway flag from persistent RAM)
; "Level beaten" flag is not set, it's not used anyway.
org $048F61
	ldx $04
	lda.l $40D000,x
	and #$00FF
	ldx !Segment
	clc
	adc.l !cDataPointerOffsets,x
	tax
	jsl ClearMidwayFlag
	warnpc $048F77

; Read midway and set entrance to midway if relevant.
org $05D9D4
	rep #$30
	jsl ReadMidwayFlag
	sep #$30
	warnpc $05D9DC

; Midway object creation code.
org $0DA68D
-	rts
	rep #$30
	jsl ReadMidwayFlag
	sep #$30
	ora $73CE
	bne -
	nop #3
	warnpc $0DA69E

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

org !cCodeClearMidways
ClearMidwayFlags:
.Initial
	jsr $8A4E
.Clear
	php
	rep #$30
	lda #$0000
	ldx #$02FE
-	sta.l !Midway,x
	dex
	dex
	bpl -
	lda #$0001
	sta.l !Midway+$00C5
	plp
	rts
warnpc !cCodeClearMidwaysEnd

org !cCodeMidway
SetMidwayFlag:
	adc.l !cDataPointerOffsets,x
	tax
	lda.l !Midway,x
	ora #$0001
	sta.l !Midway,x
	rtl

ClearMidwayFlag:
	lda.l !Midway,x
	and #$FFFE
	sta.l !Midway,x
	rtl

ReadMidwayFlag:
	lda !Segment
	and #$000E
	tax
	lda $73BF
	clc
	adc.l !cDataPointerOffsets,x
	tax
	lda.l !Midway,x
	and #$0001
	rtl
warnpc !cCodeMidwayEnd