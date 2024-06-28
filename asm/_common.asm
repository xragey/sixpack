;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;
; SIX PACK by Ragey
; _common.asm
;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; Constants

!cExits = 622
!cCountStagesWithGFX33Altered = 12

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

; (Free)RAM addresses
!OverworldIndex = $60
!Map16RemapTableHigh = $3500
!YoshiWingsTargetLevel = $6DC3
!DemoTimer = $6DD9
!MarioLuigiPalettePtr = $6F5E
!SwitchPalaceCursor = $73F2
!LightningGenerator = $7864
!Segment = $7F2B
!ExitCount = $7F2D
!NoUploadSamples = $4001C0
!Warning = $4001C1
!Midway = $40C000
!Map16RemapTableLow = $404000
!TileGen0Low = $404200
!TileGen0High = $404210
!TileGen1Low = $404220
!TileGen1High = $404230
!TileBerries = $404240
!PersistentExitFlags = $41C400
!PersistentExitCount = $41C08B
!TitleScreenStageIndex = $7F9C7E

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

!cCodeDisableCredits = $009468
!cCodeDisableCreditsEnd = !cCodeDisableCredits+8
!cCodeNintendoPresents = !cCodeDisableCreditsEnd
!cCodeNintendoPresentsEnd = !cCodeNintendoPresents+19
!cCodeTitleScreenExit = !cCodeNintendoPresentsEnd
!cCodeTitleScreenExitEnd = !cCodeTitleScreenExit+66
!cCodeDemoReel = !cCodeTitleScreenExitEnd
!cCodeDemoReelEnd = !cCodeDemoReel+60
!cCodeClearMidways = !cCodeDemoReelEnd
!cCodeClearMidwaysEnd = !cCodeClearMidways+29
!cCodeOwPalette = !cCodeClearMidwaysEnd
!cCodeOwPaletteEnd = !cCodeOwPalette+12
!cCodeSramBank0 = !cCodeOwPaletteEnd
!cCodeSramBank0End = !cCodeSramBank0+53
!cCodeGfx33Handler = !cCodeSramBank0End
!cCodeGfx33HandlerEnd = !cCodeGfx33Handler+83
!cCodeWarning = !cCodeGfx33HandlerEnd
!cCodeWarningEnd = !cCodeWarning+100
!cCodeScrollCrash = !cCodeWarningEnd
!cCodeScrollCrashEnd = !cCodeScrollCrash+20
!cCodeCheckObjectBank00 = !cCodeScrollCrashEnd
!cCodeCheckObjectBank00End = !cCodeCheckObjectBank00+47
assert !cCodeCheckObjectBank00End < $00968E

!cCodeBonusGame = $0195FC
!cCodeBonusGameEnd = !cCodeBonusGame+32
assert !cCodeBonusGameEnd < $019620

!cCodePSwitchColour = $01E2B0
!cCodePSwitchColourEnd = !cCodePSwitchColour+17
!cCodeBowser = !cCodePSwitchColourEnd
!cCodeBowserEnd = !cCodeBowser+12
assert !cCodeBowserEnd < $01E2CF

!cDataGfx33Identifiers = $01FFC0
!cDataGfx33Users = $01FFE0

!cCodeSpriteThruPipes = $02B5EC
!cCodeSpriteThruPipesEnd = !cCodeSpriteThruPipes+42
assert !cCodeSpriteThruPipesEnd < $02B630

; $02D51E is used for registration
!cCodeLightningCall = $02FFE2
!cCodeLightningCallEnd = !cCodeLightningCall+26
assert !cCodeLightningCallEnd < $02FFFF

!cDataPointerOffsets = $03BDA0
!cDataPointerOffsetsEnd = !cDataPointerOffsets+48
!cCodeStageNameIndex = !cDataPointerOffsetsEnd
!cCodeStageNameIndexEnd = !cCodeStageNameIndex+64
!cCodeMessages = !cCodeStageNameIndexEnd
!cCodeMessagesEnd = !cCodeMessages+12
!cCodeDrawAuthorName = !cCodeMessagesEnd
!cCodeDrawAuthorNameEnd = !cCodeDrawAuthorName+80
!cCodeBowserSamples = !cCodeDrawAuthorNameEnd
!cCodeBowserSamplesEnd = !cCodeBowserSamples+9
assert !cCodeBowserSamplesEnd < $03BE80

!cCodeOverworldProgress = $049AC5
!cCodeOverworldProgressEnd = !cCodeOverworldProgress+325
!cCodeLightning = !cCodeOverworldProgressEnd
!cCodeLightningEnd = !cCodeLightning+170
!cCodeLineGuideFix = !cCodeLightningEnd
!cCodeLineGuideFixEnd = !cCodeLineGuideFix+72
assert !cCodeLineGuideFixEnd < $049D06

!cCodePointerLogicBank05 = $058E19
!cCodePointerLogicBank05End = !cCodePointerLogicBank05+46
!cCodeYoshiWingsRoute = !cCodePointerLogicBank05End
!cCodeYoshiWingsRouteEnd = !cCodeYoshiWingsRoute+32
!cCodeSwitchDialog = !cCodeYoshiWingsRouteEnd
!cCodeSwitchDialogEnd = !cCodeSwitchDialog+159
!cCodeTileGen = !cCodeSwitchDialogEnd
!cCodeTileGenEnd = !cCodeTileGen+75
!cCodeSideExit = !cCodeTileGenEnd
!cCodeSideExitEnd = !cCodeSideExit+33
!cCodePiranhaPropertyByte = !cCodeSideExitEnd
!cCodePiranhaPropertyByteEnd = !cCodePiranhaPropertyByte+95
!cCodeTally = !cCodePiranhaPropertyByteEnd
!cCodeTallyEnd = !cCodeTally+37
assert !cCodeTallyEnd < $058FFF

!cDataDemoReel = $0DF300
!cDataDemoReelEnd = !cDataDemoReel+1536
!cCodeMidway = !cDataDemoReelEnd
!cCodeMidwayEnd = !cCodeMidway+53
!cCodeRemap16 = !cCodeMidwayEnd
!cCodeRemap16End = !cCodeRemap16+533
!cCodeYoshiWingsObject = !cCodeRemap16End
!cCodeYoshiWingsObjectEnd = !cCodeYoshiWingsObject+33
!cCodeMarioPaletteObject = !cCodeYoshiWingsObjectEnd
!cCodeMarioPaletteObjectEnd = !cCodeMarioPaletteObject+33
!cCodeAutosave = !cCodeMarioPaletteObjectEnd
!cCodeAutosaveEnd = !cCodeAutosave+122
!cCodeCheckObjectBank0D = !cCodeAutosaveEnd
!cCodeCheckObjectBank0DEnd = !cCodeCheckObjectBank0D+25
assert !cCodeCheckObjectBank0DEnd < $0DFE9F

!cCodeSa1Main = $0E84D0
!cCodeSa1MoreSprites = $0ECA92
!cCodeSa1NMSTL = $0ED170
!cCodeSa1End = $0ED1B4
!cCodeDecompressPalette = !cCodeSa1End
!cCodeDecompressPaletteEnd = $0ED255

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

!cDataSpritePointers       = $05E000
!cDataSpriteBankPointers   = $068260
!cDataLayer1Pointers       = $069260
!cDataLayer2Pointers       = $06C260
!cDataPalettePointers      = $0780C3
!cDataStageExAnimPointers  = $07B0C3
!cDataMessagePointers      = $07E0C3
!cDataCustomMarioPalettes  = $0FECC3
; Unused: $07EFC3--$07EFFF
!cDataStageHeader0EF310    = $0C8000
!cDataAuthorNames          = $0C9000
!cDataContestNumbers       = $0CD500
!cDataStageHeader05DE00    = $0ED255
; Unused: $0EE255--$0EF0FF
!cDataStageHeader05F000    = $0FA654
!cDataStageHeader05F200    = $0FB654
!cDataStageHeader05F400    = $0FC654
!cDataStageHeader05F600    = $0FD654
; Unused: $0FE654--$0FEF9E
; Unused: $C00000--$C0C6FF (Note that second header is in this range)
!cDataStageNames           = $C0C700
!cDataGraphicsBypass0      = $C10000
!cDataGraphicsBypass4      = $C20000
!cDataStageHeader06FC00    = $C30000
!cDataStageHeader06FE00    = $C31000
!cDataStageHeader03FE00    = $C32000
!cPaletteData              = $C33000 ; Ends at $C3FFFF
!cDataMessages             = $FF0000
!cDataMarioLuigiPalette    = $FFE000

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

padbyte $FF

