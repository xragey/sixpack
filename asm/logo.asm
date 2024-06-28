;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; SIX PACK by Ragey
; logo.asm
;
; Changes the colour of the "Nintendo Presents" logo.
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

incsrc "_common.asm"
fullsa1rom

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; Set the color of the "Nintendo presents" icon.
org $0093D7
	jsr NintendoPresents

org !cCodeNintendoPresents
NintendoPresents:
	jsr $ABED
	lda $6100
	bne +
	lda #$7C
	sta $6806
	lda #$00
	stz $6805
+	rts
	warnpc !cCodeNintendoPresentsEnd
