;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; SIX PACK by Ragey
; demo.asm
;
; Implements random stage display on the title screen.
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

incsrc "_common.asm"
fullsa1rom

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

org $009337
	dw GameMode07

org $009C1F
GameMode07:
	jsr $9A74
	jsr $9CBE
	bne OpenMenu
	jsr $F62D
	lda $13
	and #$03
	bne +
	dec !DemoTimer
	lda !DemoTimer
	beq ReloadTitleScreen
+	lda $71
	cmp #$09
	bne +
	lda $7496
	cmp #$01
	beq ReloadTitleScreen
+	lda #$02
	sta $6F31
	jmp $A1E4					; Run game mode 14, skipping message box logic
	warnpc $009C89

org $009C89
ReloadTitleScreen:

org $009C8F
CheckMusicChange:
	phx
	ldx $6100
	cpx #$0B
	bcc +
	sta $7DFB
+	plx
	rts
warnpc $009C9C

org $009C9F
OpenMenu:

org $0096CB
SetTitleScreenStage:
	ldy #$00
	sty $7F11
	jsl SelectRandomTitleStage
	nop
warnpc $009C9E

org $00F60C
	jsr CheckMusicChange

org !cCodeDemoReel
SelectRandomTitleStage:
	rep #$30
	lda !TitleScreenStageIndex
	and #$01FF
	inc a
	cmp #$01E0					; 480 demo stages (cutscenes removed), change if this count changes
	bcc +
	sec
	sbc #$01E0
+	sta !TitleScreenStageIndex
	tax
	sep #$20
	lda.l !cDataDemoReel,x
	and #$0F
	sta !Segment
	lda.l !cDataDemoReel+768,x
	sta $6109
	sep #$10
	lda #$C0
	sta !DemoTimer
	rtl
warnpc !cCodeDemoReelEnd
