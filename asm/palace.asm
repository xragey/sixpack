;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; SIX PACK by Ragey
; palace.asm
;
; Implements an overworld menu to toggle Switch Palace status. This repurposes
; (and replaces) the logic for the save prompt, which is not used in Six Pack.
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

incsrc "_common.asm"
fullsa1rom

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; Allow the user to bring up the prompt by pressing SELECT.
org $048244
GameMode0E:
	ldx $6DB3
	lda $6DA6,x
	and #$20
	beq +
	lda $7B87
	bne +
	lda #$05
	sta $7B87
	nop #12
+	warnpc $048264

; Do not write layer 3 text when opening the prompt.
org $04F439
	nop #4

; Implement prompt logic.
org $009BA8
SwitchPalacePrompt:
	lda $16
	bit #$20
	bne .Select
	inc $7B91
	jsl InteractSwitchPalacePrompt
	jsl DrawSwitchPalacePrompt
	rtl

.Select
	jml $009C13
	rtl
	warnpc $009BC8

; Handle pressing any button other than SELECT while prompt is open.
org !cCodeSwitchDialog
InteractSwitchPalacePrompt:
	bit #$02
	bne .Left
	bit #$01
	bne .Right
	ora $18
	bit #$80
	beq .Return

.AorB
	ldx #$0B
	stx $7DF9
	ldx !SwitchPalaceCursor
	lda #$01
	eor $7F27,x
	sta $7F27,x
	rtl

.Left
	dec !SwitchPalaceCursor
	bra +

.Right
	inc !SwitchPalaceCursor
+	lda #$03
	and !SwitchPalaceCursor
	sta !SwitchPalaceCursor
	ldx #$06
	stx $7DFC

.Return
	rtl

DrawSwitchPalacePrompt:
	; Draw cursor.
	lda $7B91
	eor #$1F
	and #$18
	beq +
	ldx !SwitchPalaceCursor
	lda.l .SwitchPalaceXPosition,x
	sta $6300
	lda #$60
	sta $6301
	lda #$6A
	sta $6302
	lda #$38
	sta $6303
	lda #$02
	sta $6460

+	; Draw switches.
	ldx #$00
	ldy #$00
-	lda.l .SwitchPalaceXPosition,x
	sta $6304,y
	lda #$78
	sta $6305,y
	lda $7F27,x
	beq +
	lda #$06
+	eor #$2A
	sta $6306,y
	lda.l .SwitchPalaceProperties,x
	sta $6307,y
	iny #4
	inx
	cpx #$04
	bcc -
	lda #$02
	sta $6461
	sta $6462
	sta $6463
	sta $6464
	rtl

.SwitchPalaceXPosition
	db $48,$68,$88,$A8
.SwitchPalaceProperties
	db $38,$3A,$3C,$3E
	warnpc !cCodeSwitchDialogEnd

; Rearrange OAM map. Needed because MaxTile (SA-1) messes with this logic.
org $00A169
	lda #$80
	sta $3F