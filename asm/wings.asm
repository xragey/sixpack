;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; SIX PACK by Ragey
; wings.asm
;
; Changes the engine to allow dynamic routing for the Yoshi wings levels. Also
; implements extended object 0x5 which can be used to set the level to warp to.
; As always, can only warp within the currently active segment.
;
; Extended object 0x5 format:
;   000LLLLL 0000llll 00000101
;   * Ll (0-0x1FF) is the level to teleport to within the current segment.
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

incsrc "_common.asm"
fullsa1rom

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

org $0DA11E
	dl ExtendedObject05

org !cCodeYoshiWingsObject
ExtendedObject05:
	lda $65
	pha
	sec
	sbc #$03
	sta $65
	ldy #$00
	lda [$65],y
	asl #4
	iny
	ora [$65],y
	sta !YoshiWingsTargetLevel
	lda #$00
	adc #$00
	sta !YoshiWingsTargetLevel+1
	pla
	sta $65
	rts
	warnpc !cCodeYoshiWingsObjectEnd

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

org $05DBC6
	jmp RouteYoshiWings

org !cCodeYoshiWingsRoute
RouteYoshiWings:
	cpy #$01
	bne +
	; Load a Yoshi wings level...
	lda !YoshiWingsTargetLevel
	bne ++
	; Load default Yoshi wings level if nothing defined ($1C8)
	lda #$C8
	sta $79B8,x
	lda #$04
	sta $79D8,x
	rts
++	; Load user-defined Yoshi wings level otherwise
	sta $79B8,x
	lda !YoshiWingsTargetLevel+1
	ora #$04
	sta $79D8,x
+	rts
	warnpc !cCodeYoshiWingsRouteEnd
