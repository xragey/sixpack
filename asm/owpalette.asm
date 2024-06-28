;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; SIX PACK by Ragey
; owpalette.asm
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

incsrc "_common.asm"
fullsa1rom

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

org $00AD2A
	jsl $00B2C8 ; mariopalette.asm
	jsr CheckLoadSpecialPalette
	nop
	warnpc $00AD32	

org !cCodeOwPalette
CheckLoadSpecialPalette:
	lda !ExitCount
	cmp.w #!cExits
	bcc +
	ora #$8000
+	rts
	warnpc !cCodeOwPaletteEnd