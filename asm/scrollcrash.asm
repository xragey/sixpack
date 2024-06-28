;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; SIX PACK by Ragey
; scrollcrash.asm
;
; Fixes issue that occurs when LR scrolling an autoscroll sprite into range.
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

incsrc "_common.asm"
fullsa1rom

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

org $00CDDD
	lda $9D
	jsr LRScrollFix

org !cCodeScrollCrash
LRScrollFix:
	and $73FD
	beq +
	lda $7411
	bne ++
	stz $9D
+	lda $7411
	bne ++
	pla
	pla
++	rts
	warnpc !cCodeScrollCrashEnd
