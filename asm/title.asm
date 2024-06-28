;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; SIX PACK by Ragey
; title.asm
;
; Implements random stage selection and display on the Title Screen.
;
; Also remaps text tiles and properties (MARIO A, ERASE FILE, etc) to fit with
; the rearranged title screen and the changed palette logic.
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

incsrc "_common.asm"
fullsa1rom

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; Prevent background color change when going to or from the ERASE FILE menu.
org $009B1A : nop #10
org $009CD1 : nop #10

; Do not allow the player to skip the opening circle animation on the title
; screen. This somehow conflicts with level loading and may show the level in a
; mid-loading state. It may be related to remap16.asm, but I'm not sure.
org $009421 : db $80

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; Support a 16-bit exit counter.
org $009D66
FileSelectExitCounter:
	rep #$20
	ldy #$38FC
	lda.l !PersistentExitCount,x
	sta $4204
	cmp.w #!cExits
	bcc +
	ldy #$3C87
+	tya
	sep #$10
	ldx $00
	sta.l $7F837F,x
	ldy #$64
	sty $4206
	nop #8
	lda $4214
	asl
	tay
	lda.w Digits,y
	sta.l $7F8381,x
	lda $4216
	ldy #$0A
	jsr ContinueFileSelectExitCounter
	sep #$20 
	warnpc $009DA6

org !cCodeTitleScreenExit
ContinueFileSelectExitCounter:
	sta $4204
	sty $4206
	nop #8
	lda $4214
	asl
	tay
	lda.w Digits,y
	sta $7F8383,x
	lda $4216
	asl
	tay
	lda.w Digits,y
	sta $7F8385,x
	lda #$38FC
	sta $7F8387,x
	rts
	
Digits:
	dw $3C29,$3D6D,$3D6E,$3C4E,$3C50,$3C51,$3C52,$3C53
	dw $3C2A,$3C2B
warnpc !cCodeTitleScreenExitEnd

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

org $05B6FE	; Clear text area
	db $51,$85,$40,$2E,$FC,$38
	db $51,$A8,$40,$1C,$FC,$38
	db $51,$C5,$40,$2E,$FC,$38
	db $51,$E8,$40,$1C,$FC,$38
	db $52,$05,$40,$2E,$FC,$38
	db $52,$45,$40,$1C,$FC,$38

org $05B722	; MARIO A ...EMPTY
	db $51,$8D,$00,$1F,$76,$3D,$71,$3D
	db $74,$3D,$82,$3C,$83,$3C,$FC,$38
	db $71,$3D,$FC,$38,$74,$3C,$74,$3C
	db $74,$3C,$73,$39,$76,$39,$6F,$39
	db $2F,$39,$72,$39

org $05B746	; MARIO B ...EMPTY
	db $51,$CD,$00,$1F,$76,$3D,$71,$3D
	db $74,$3D,$82,$3C,$83,$3C,$FC,$38
	db $2C,$3D,$FC,$38,$74,$3C,$74,$3C
	db $74,$3C,$73,$39,$76,$39,$6F,$39
	db $2F,$39,$72,$39

org $05B76A	; MARIO C ...EMPTY
	db $52,$0D,$00,$1F,$76,$3D,$71,$3D
	db $74,$3D,$82,$3C,$83,$3C,$FC,$38
	db $2D,$3D,$FC,$38,$74,$3C,$74,$3C
	db $74,$3C,$73,$39,$76,$39,$6F,$39
	db $2F,$39,$72,$39

org $05B78E	; ERASE A
	db $51,$87,$00,$0B,$73,$3D,$74,$3D
	db $71,$3D,$31,$3D,$73,$3D,$FC,$38

org $05B79E	; ERASE B
	db $51,$C7,$00,$0B,$73,$3D,$74,$3D
	db $71,$3D,$31,$3D,$73,$3D,$FC,$38

org $05B7AE	; ERASE C
	db $52,$07,$00,$0B,$73,$3D,$74,$3D
	db $71,$3D,$31,$3D,$73,$3D,$FC,$38

org $05B7BE	; END
	db $52,$47,$00,$05,$73,$3D,$79,$3C
	db $7C,$3C,$FF

org $05B7C9	; Clear text area
	db $51,$85,$40,$2E,$FC,$38
	db $51,$A8,$40,$1C,$FC,$38
	db $51,$C5,$40,$2E,$FC,$38
	db $51,$E8,$40,$1C,$FC,$38
	db $52,$05,$40,$2E,$FC,$38
	db $52,$45,$40,$1C,$FC,$38

org $05B7ED	; MARIO A ...EMPTY
	db $51,$8A,$00,$1F,$76,$3D,$71,$3D
	db $74,$3D,$82,$3C,$83,$3C,$FC,$38
	db $71,$3D,$FC,$38,$74,$3C,$74,$3C
	db $74,$3C,$73,$39,$76,$39,$6F,$39
	db $2F,$39,$72,$39

org $05B811	; MARIO B ...EMPTY
	db $51,$CA,$00,$1F,$76,$3D,$71,$3D
	db $74,$3D,$82,$3C,$83,$3C,$FC,$38
	db $2C,$3D,$FC,$38,$74,$3C,$74,$3C
	db $74,$3C,$73,$39,$76,$39,$6F,$39
	db $2F,$39,$72,$39

org $05B835	; MARIO C ... EMPTY
	db $52,$0A,$00,$1F,$76,$3D,$71,$3D
	db $74,$3D,$82,$3C,$83,$3C,$FC,$38
	db $2D,$3D,$FC,$38,$74,$3C,$74,$3C
	db $74,$3C,$73,$39,$76,$39,$6F,$39
	db $2F,$39,$72,$39

org $05B859	; ERASE DATA
	db $52,$4A,$00,$13,$73,$3D,$74,$3D
	db $71,$3D,$31,$3D,$73,$3D,$FC,$38
	db $7C,$3C,$71,$3D,$2F,$3D,$71,$3D
	db $FF

org $05B872	; Clear text area
	db $51,$85,$40,$2F,$FC,$38
	db $51,$C5,$40,$2F,$FC,$38
	db $52,$05,$40,$2F,$FC,$38
	db $52,$45,$40,$1C,$FC,$38

org $05B88A	; 1 PLAYER GAME
	db $51,$AA,$00,$19,$6D,$3D,$FC,$38
	db $6F,$3D,$70,$3D,$71,$3D,$72,$3D
	db $73,$3D,$74,$3D,$FC,$38,$75,$3D
	db $71,$3D,$76,$3D,$73,$3D

org $05B8A8	; 2 PLAYER GAME
	db $51,$EA,$00,$19,$6E,$3D,$FC,$38
	db $6F,$3D,$70,$3D,$71,$3D,$72,$3D
	db $73,$3D,$74,$3D,$FC,$38,$75,$3D
	db $71,$3D,$76,$3D,$73,$3D

org $009E74 ; Cursor positions
	db $CB,$51
	db $88,$51
	db $A8,$51
	db $C4,$51
	db $85,$51

org $009EC0	; Cursor properties
	lda.w #$3920

org $00B62C	; Title screen palette 1, colors 8-F
	dw $437F,$1CFF,$6318,$0000,$437F,$173F,$7FFF,$0000

org $00B63C	; Title screen palette 0, colors 8-F
	dw $437F,$7F60,$0320,$0000,$437F,$5BBF,$327B,$08E7
