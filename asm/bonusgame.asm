;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; SIX PACK by Ragey
; bonusgame.asm
;
; There's one level that ends with a bonus game. This allows that level to exit
; properly despite this error.
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

incsrc "_common.asm"
fullsa1rom

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

org $01DDAC
	jsr InitBonusGame

org !cCodeBonusGame
InitBonusGame:
	lda !Segment
	cmp #$0E
	bne +
	lda $73BF
	cmp #$46
	bne +
	lda #$01
	sta $6DD5
	sta $7DE9
	sta $73CE
	sta $7425
+	lda $7B94
	rts
	warnpc !cCodeBonusGameEnd