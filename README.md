# Borderlands Commander
A Windows program that provides a number of useful functions while playing Borderlands 2 and TPS:
* Saving and teleporting your position in the game.
* Freezing time.
* Modifying game speed.
* Toggling HUD elements.
* Toggling Third Person camera.

See the video below for a brief demonstration.

[![Borderlands Commander Intro](https://i.imgur.com/ZY1nw1z.jpg)](https://youtu.be/ftfeGFUteWI)

This is made possible thanks to [c0dycode's CommandInjector](https://github.com/c0dycode/BL-CommandInjector), via the [BLIO set of methods](https://github.com/mopioid/BLIO). Also thanks to LightChaosman and his [NoDamageNumbers mod](https://github.com/BLCM/BLCMods/blob/master/Borderlands%202%20mods/LightChaosman/NoDamageNumbers.txt), FromDarkHell for various modding tidbits, and JoltzDude139 for expert testing and feedback.

## Installation

For Borderlands Commander to be able to interact with the game, you must add a few things to the game's Win32 folder. If you already have CommandInjector installed, you are all set to go and may skip ahead to [using Borderlands Commander](#usage)!

1. Quit the game if it is running.
2. [Download the latest version of `ddraw.dll` (A.K.A. PluginLoader).](https://github.com/c0dycode/BorderlandsPluginLoader/releases)
3. Locate the `Win32` folder within your game's `Binaries` folder. ![Win32 folder](https://i.imgur.com/t6OI06l.png)

4. Copy `ddraw.dll` to the `Win32` folder. ![ddrawl.dll](https://i.imgur.com/FHfiSqg.png)

5. In the `Win32` folder, create a folder called `Plugins`. ![Plugins folder](https://i.imgur.com/CDdoKDs.png)

7. [Download the latest version of CommandInjector.](https://github.com/c0dycode/BL-CommandInjector/blob/master/CommandInjector.zip)

6. Open the `CommandInjector.zip` file to view its contents. ![CommandInjector.zip](https://i.imgur.com/r1I3b26.png)

7. Copy `CommandInjector.dll` (BL2) or `CommandInjectorTPS.dll` (TPS) to the `Plugins` folder you created. ![CommandInjector.dll](https://i.imgur.com/U9OSqcV.png)

## Usage

Borderlands Commander is a simple program that you may store in whatever folder you would like.

To start using Borderlands Commander, simply launch the program (BL2 or TPS do not need to already be running). Upon launch, it will exist as an icon in your system tray. You may now use all of its functionality!

### Settings

Right clicking the system tray icon provides all of Borderlands Commander's settings. ![Borderlands Commander Settings](https://i.imgur.com/SiXMOIU.png)

The "Show Feedback" option tells Borderlands Commander to print out details in game when you use some of its functions.
![Feedback](https://i.imgur.com/2m4RA4x.png)

The "Symbol Bindings" and "Numpad Bindings" options choose which set of key bindings Borderlands Commander will use. See below.

### Symbol Bindings

| Key  | Function |
| ------------- | ------------- |
| \[ | Halve Game Speed  |
| \] | Double Game Speed  |
| \\ | Reset Game Speed  |
| ,  | Restore position  |
| .  | Save position  |
| /  | Toggle Players Only Mode  |
| ;  | Toggle HUD  |
| '  | Toggle Damage Numbers  |
| =  | Toggle Third Person  |
| F7 | Toggle All Key Bindings  |

### Numpad Bindings

| Key  | Function |
| ------------- | ------------- |
| 1  | Halve Game Speed  |
| 2  | Double Game Speed  |
| 3  | Reset Game Speed  |
| 4  | Restore position  |
| 5  | Save position  |
| 6  | Toggle Players Only Mode  |
| 7  | Toggle HUD  |
| 8  | Toggle Damage Numbers  |
| 9  | Toggle Third Person  |
| F7 | Toggle All Key Bindings  |
