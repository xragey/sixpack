;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; SIX PACK by Ragey
; misc.asm
;
; Implements several small engine changes.
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

incsrc "_common.asm"
fullsa1rom

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; Do not suppress sample upload on game boot. (This code is cleared by SA-1 so
; it's free real estate for us!)
org $008027
	lda.w #$0000
	sta.l !NoUploadSamples
	sta !Warning

; Disable intro level, go straight to jail.
org $009CB1 : db $00

; Disable message upon saving Yoshi for the first time.
org $01EC3B : nop #5

; Spawn Switch Palace objects regardless of whether or not they're pressed.
org $0DEC9A : nop #2

; Have Switch Palaces always work, even if already pressed.
org $00EEAE
	nop #4
	lda #$01

; Do not display a text message for a Switch Palace, just return to map.
org $00C956
	stz $73D2
	nop #2

org $00EECC
	lda #$FF

; Disable hardcoded overworld paths.
org $049078 : rep 10 : db $00

; Increase the amount of overwrold tiles that Mario swims on.
org $04965E : cmp.w #$0076

; Change X icon on overworld border to # icon.
org $04A530 : db $5A,$39

; Remove overworld clouds.
org $04FB37 : rts

; Revert Lunar Magic 3.00+ change to layer 2 scroll settings, which is
; incompatible with certain old levels.
org $05D710
	db $03,$01,$01,$00,$00,$02,$02,$01
	db $00,$00,$00,$00,$00,$00,$00,$00
	db $02,$02,$01,$00,$01,$02,$01,$00
	db $00,$00,$00,$00,$00,$00,$00,$00

; Revert Lunar Magic 3.00+ fix to layer 2, that (correctly) sets layer 2
; X position to 0 on loading a sublevel whose X-scroll setting is None.
; Some older entries depend on this (broken) behaviour.
org read3($05DA18)
	skip 27
	nop #2

; Never autowalk on the overworld.
org $049212 : db $80

; Don't force No Yoshi intro for levels with translevel ID >$52.
org $05DA1E : db $80

; Actually, just don't show the No Yoshi intro at all.
org $05DA3B : db $80

; Never show TIME UP! message (even if time was up).
org $00D0F1 : db $80

; Don't implement Yoshi's House message logic.
; (Note that no level uses this, so there's no need to implement this logic.)
org $05B1D3 : db $80

; Never have level #$13 activate a secret exit on boss defeated.
; (Note that no level uses this, so there's no need to implement this logic.)
org $00CA0D : db $80

; Never have the ledge Dry Bones throw bones.
; (Note that no level uses this, so there's no need to implement this logic.)
org $01E52B : db $80
org $01E5A5 : db $80

; Never use slow Monty Mole logic. This is not needed because Six Pack places
; all of the level nodes on the main overworld map.
; (This one is probably used by a few entries, either intended or not. But it's
; too much work to carry this over... I'd have to check every translevel again.)
;org $01E2FB : db $20

; Omit special handling of level $24. This is not needed because Six Pack does
; not assign this level; this node is used for the tile Mario starts on.
;org $05DAE6 : db $80

; Disable credits and cutscenes.
org !cCodeDisableCredits
	ldy #$0C
	sty $6100
	jmp $A087
warnpc !cCodeDisableCreditsEnd
