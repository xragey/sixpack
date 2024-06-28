;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; SIX PACK by Ragey
; registration.asm
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

incsrc "_common.asm"
fullsa1rom

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; Build time and version number
org $02D51E
	db "Six Pack 1.1 by AaBdeehiinnnnorrssttuuWz a.k.a. Ragey - 31/12/2023 11:15                         "
	warnpc $02D599

; Primary ROM header
org $00FFC0
	db "Six Pack             "

; Secondary ROM header
org $C07FC0
	db "Six Pack             "

; Remove Lunar Magic watermark
org $0FF0A0
	rep 192 : db $00

; Emulate Lunar Magic protection
org $00FFBF
	db $42

; Build ID (also makes Lunar Magic reject the ROM)
org $00FFDB
	db $01

; Build ID in secondary header
org $C07FDB
	db $01

; Enable free roam, for debugging
;org $00CC84
;	db $F0
