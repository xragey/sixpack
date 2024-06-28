# Six Pack

Six Pack is a hack for Super Mario World. Like many hacks for this game, it patches the game to add new levels, a new overworld map, and many technical features to the game. In the case of Six Pack specifically, it patches in most of the levels that were created for the first six iterations of [SMWCentral](https://www.smwcentral.net)'s "Vanilla Level Design Contest". It contains levels created by hundreds of users, and at 495 levels, it is by far the biggest Super Mario World hack to date.

## What is this?

This is the source code used to convert a Super Mario World ROM into a Six Pack ROM. Compilation hacks of levels created by different authors are difficult and time-consuming to assemble. This project represents an experiment on automatically creating such a compilation hack. The script automatically rearranges a variety of assets into a single game. Because of the sheer size of the project, it also contains a lot of ASM hacks to expand the capabilities of the base game to handle such an enormous amount of levels, as well as some other technical additions and improvements.

## How do I play it?

Not interested in technical mumbo jumbo and just want to play? In that case, you can ignore this repository entirely and just grab a copy of the game over at the [SMWCentral hack repository](https://www.smwcentral.net/?p=section&a=details&id=35347). The only things you'll need are a clean Super Mario World ROM, a BPS patching utility, and an emulator. You can find all of these on the Internet. Do not ask me about any of these.

## How does it work?

Note that the repository does not work as-is as it depends on the presence of several files that I do not include within the repository for a variety of reasons (usually copyright). You will need to add these yourself.

In `base/BaseGraphics/`, place the graphics files as they would be extracted by Lunar Magic (`GFX00.bin`--`GFX33.bin` with the berry tile converted). Also include a file `GFX01-AltBerry.bin` with the berry tile _not_ converted.

In `base/ExGraphics/`, place files `ExGFX80.bin`--`ExGFX87.bin`. These contain a mixture of custom graphics and original Super Mario World graphics, which is why they're not included. Either extract them from a build of Six Pack yourself, or just place dummy files (4kB in size) here.

In `base/Graphics/`, place files `GFX00.bin`--`GFX33.bin`. As above, these are not included because they contain original Super Mario World graphics. Either extract them from Six Pack yourself or just copy the contents of `base/BaseGraphics/` to this folder.

In `base/level/`, place the 512 original `.mwl` levels, named `_ 000.mwl`--`_ 1FF.mwl`. Lunar Magic can do this for you.

The `bin/` folder should include binaries for Asar (named `asar.exe`), Floating IPS (named `flips.exe`), and Modern Recover Lunar Magic (named `mrlm.exe`).

The `input/patch/#/` folders contain the levels to assemble as IPS or BPS patches, for example `input/patch/1/mylevel.ips`. Use the `fromsource.py` script to further populate the `input/` folder with GFX, Map16, MWL, and ROM resources.

The `input/demo.txt` file states which levels will be cycled through in the demo, and the `input/translevels.txt` file lets the scripts know which files hold the translevel (first level entered from the overworld) for each entry.

The `music` folder contains an installation of AddmusicK. You can download a version of AddmusicK from the Internet. When filling in `Addmusic_list.txt`, keep in mind that track 15 is used for the title screen and track 29 is used for a dummy track representing silence.

The `override/map16/` and `override/mwl/` folders are used to override these resources for levels. For example, if `override/mwl/mylevel 105.mwl` exists and the assembly process encounters a file with the name `mylevel 105.mwl` it will discard that file and use the file override here instead. (The map16 override works the same). Six Pack uses this to manually fix some issues in some levels that are part of the compilation. The overrides are not included in this repository.

The `script/` folder contains the Python scripts used to compile the hack. Use `script/fromsource.py` to prepare the `input/` folder, and then `script/prepare.py` to build a Six Pack ROM.

The `work/` folder is where `script/prepare.py` outputs the files it generates. In the case of Six Pack, it creates one image with all of the levels inserted (`SixPack.smc`) and eight images each with a subset of the levels inserted (`Segment0.smc`--`Segment7.smc`). The Segments images can be opened in Lunar Magic to inspect the output.

## "It works on my machine"

The source code in this repository is provided to you in the hopes it will be useful, but without any guarantees.
Do not ask me questions about how anything in this repository works. I consider this project finished and haven't touched it in a while. Chances are if you can't get it to work, I have forgotten how to as well.

## Some other remarks

In case it wasn't obvious yet, I am not affiliated with Nintendo.
I am also not affiliated with SMWCentral other than being a member of the community there.

