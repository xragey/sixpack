;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; SIX PACK by Ragey
; bowser.asm
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

incsrc "_common.asm"
fullsa1rom

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; The fireworks runs some preparation code for the credits sequence. If we omit
; running this, it makes Bowser behave like a normal boss
org $00C5C0
	nop #11

; Suppress AddmusicK sample upload to prevent pause between Bowser phases
org $03A25D
	jsr SuppressSampleUpload

org !cCodeBowserSamples
SuppressSampleUpload:
	lda #$01
	sta !NoUploadSamples
	jmp $A279
	warnpc !cCodeBowserSamplesEnd

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; Bowser outside of a designated mode 7 room seems to act different between a
; sa1 rom and a normal rom. One entry uses bowser like this, so let's fix that.
org $03A113
	jsl ConditionalBowsah

org !cCodeBowser
ConditionalBowsah:
	lda $6D9B
	cmp #$C1
	bne +
	jsl $03DD7D
+	rtl
	warnpc !cCodeBowserEnd



	