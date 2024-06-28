;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; SIX PACK by Ragey
; creatingblock.asm
;
; Three levels use this. One of them is the submap one, two is for the main map.
;
; Chrominus Castle (Segment #$06)
; Wowfunhappy (Segment #$00)
; ...tbd
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

incsrc "_common.asm"
fullsa1rom

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

org $0392F8
	phx
	ldy $32B0,x
	inc $32B0,x
	lda $93A4,y ; Submap route (Chrominus Castle)
	ldx !Segment
	cpx #$06
	bra +
	lda $93EF,y ; Main map route 
+	plx
	nop
	warnpc $03930E
