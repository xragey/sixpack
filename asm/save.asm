;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; SIX PACK by Ragey
; save.asm
;
; Handles (auto)saving whenever the overworld is loaded.
; Note that midway points are not saved.
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

incsrc "_common.asm"

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; "Check if file is blank" routine.
org $009D61 : jsr BlankFile

org !cCodeSramBank0
FileBitMask:
	dw $FCFC,$F3F3,$CFCF,$3F3F

BlankFile:
	stx $0E				; File
	jsr $9DB5			; Check if file is blank
	php
	beq +
	rep #$30
	lda $0E				; File
	and #$0003
	asl
	tax
	lda #$0000
	sta.l !ExitCount,x
	txy
	ldx #$02FE
-	lda.l !PersistentExitFlags,x
	and FileBitMask,y
	sta.l !PersistentExitFlags,x
	dex
	dex
	bpl -
+	plp	
	rts
warnpc !cCodeSramBank0End

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;


; Do not increase event counter in vanilla code.
org $04EA1E : nop #3
org $00A0F9 : db $80

; Always work on the SRAM buffer.
org $04903F : nop #2
org $049051 : nop #3

; Note that $00A149 is a nicer place for this hijack as Lunar Magic NOPs it.
; But it does so on every save. Maybe it can be moved later.
org $00A15A
	jsl LoadOverworld

org !cCodeAutosave
LoadOverworld:
	; Restore call. Can be removed if hijack is moved to $00A149.
	jsl $05DBF2

SaveGame:
	; Modified version of $049037 that copies entire range.
	rep #$10
	sep #$20
	ldx #$008C
-	lda $7EA2,x
	sta $7F49,x
	dex
	bpl -
	sep #$10

	; Call save game routine.
	jsl $009BC9
-	rtl

OnLevelBeatenContd:
	; Clear midway flag
	lda.l !Midway,x
	and #$FE
	sta.l !Midway,x

	; If this exit was not registered by the scripts, do not count it. Sadly I have to
	; do this a bit roundabout because I store the bits in a different order from what
	; would be convenient here, but I don't want to change this to break other code
	; and older SRAM files.
	lda.l !cDataDemoReel,x
	lsr #6
	phx
	tax
	lda.l InvertExitBits,x
	plx
	and $6DD5
	beq -
	
	; Move to save file bits
	lda $610A
	tay
	lda $6DD5
-	dey
	bmi +
	asl #2
	bra -
+	sta $00


	lda.l !PersistentExitFlags,x
	bit $00
	bne +
	rep #$20
	inc !ExitCount
	pha
	lda !ExitCount
	cmp.w #!cExits
	bne ++
	lda #$000B
	sta $6100
++	pla
	sep #$20
+	ora $00
	sta.l !PersistentExitFlags,x
	sep #$10
	jml SaveGame

InvertExitBits:
	db $00,$02,$01,$03
warnpc !cCodeAutosaveEnd

org $048F10
	brl +
org $048F5D
	bra +
OnLevelBeaten:
	; Get offset into array
	ldx !Segment
	rep #$30
	lda !OverworldIndex
	and #$00FF
	clc
	adc.l !cDataPointerOffsets,x
	tax
	lda #$0000
	sep #$20

	jsl OnLevelBeatenContd

	; Continue normal code flow
	inc $73D9
+	jmp $9831
	warnpc $048F7E

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; Allow START+SELECTing out of the stage even if it wasn't cleared yet

org $00A261
	lda #$80
	bra +
	lda #$01
	bit $15
	bpl ++
	inc a
++	sta $73CE
	nop #15
+	warnpc $00A27E
	sta $6DD5
	inc $7DE9
	lda #$0B
	sta $6100
	rts
