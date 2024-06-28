;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; SIX PACK by Ragey
; sideways.asm
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

incsrc "_common.asm"
fullsa1rom

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

org $00E99C
	jsl SideExit

org !cCodeSideExit
SideExit:
	lda !Segment
	cmp #$02
	bne +
	lda $73BF
	cmp #$17
	bne +
	stz $6109
	lda #$01
	sta $7DE9
	sta $73CE
	lda #$01
	jmp $B165
+	jmp $B160
	warnpc !cCodeSideExitEnd