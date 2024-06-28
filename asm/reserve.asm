;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; SIX PACK by Ragey
; reserve.asm
;
; Blocks off a large segment of ROM space to prevent Lunar Magic and/or Asar
; from writing to it. This contiguous block is used to write level data into.
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

incsrc "_common.asm"
fullsa1rom
warnings disable W1019

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; Remove RATS tag protecting secondary ROM header.
org $C07FB8
	rep 8 : db $00

; Apply tags to lower area.
!__Iterator = $8A8000
while !__Iterator < $C00000
	org !__Iterator
	db "STAR"
	dw $7FF7
	dw $8008
	!__Iterator #= !__Iterator+$10000
endif

; Apply tags to higher area.
!__Iterator = $C00000
while !__Iterator < $FF8001
	org !__Iterator
	db "STAR"
	dw $FFF7
	dw $0008
	!__Iterator #= !__Iterator+$10000
endif
