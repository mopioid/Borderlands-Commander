# Borderlands Commander
An [UnrealEngine PythonSDK](https://github.com/bl-sdk/PythonSDK) mod for Borderlands 2 and Borderlands: The Pre-Sequel! that provides a number of useful functions while in game:
* Saving and teleporting your position in the game.
* Freezing time.
* Modifying game speed.
* Quitting without saving.
* Toggling HUD elements.
* Toggling Third Person camera.

See the video below for a brief demonstration.

[![Borderlands Commander Intro](https://i.imgur.com/ZY1nw1z.jpg)](https://youtu.be/ftfeGFUteWI)

This is almost entirely made possible thanks to the work of the UnrealEngine PythonSDK team. Special thanks to LightChaosman and his [NoDamageNumbers mod](https://github.com/BLCM/BLCMods/blob/master/Borderlands%202%20mods/LightChaosman/NoDamageNumbers.txt), FromDarkHell for various modding tidbits, JoltzDude139 for expert testing and feedback, and c0dycode for originally making Commander possible via [CommandInjector](https://github.com/c0dycode/BL-CommandInjector).

## Installation

Begin by [downloading the latest version of `BorderlandsCommander.zip` here](https://github.com/mopioid/Borderlands-Commander/releases).

1. [Install UnrealEngine PythonSDK](https://github.com/bl-sdk/PythonSDK#installation) if you have not already.

2. Locate the SDK's `Mods` folder (located in the `Win32` folder of the `Binaries` folder of your BL2/TPS installation).

3. Copy the `Commander` folder from `BorderlandsCommander.zip` to the SDK's `Mods` folder.

4. Launch the game, select "Mods" from the main menu, then select "Commander" to enable it.

## Usage

Borderlands Commander is operated using key inputs during gameplay. These key bindings may be configured in game via the settings menu (OPTIONS > KEYBOARD/MOUSE > MODDED KEY BINDINGS). See table for description of functionality:

| Action                | Description                                                                       |
|-----------------------|-----------------------------------------------------------------------------------|
| Halve Game Speed      | Decreases the speed of the game to 1/2, then 1/4, etc., to a minimum of 1/32      |
| Double Game Speed     | Increases the speed of the game to x2, then x4, etc., to a maximum of x32         |
| Reset Game Speed      | Resets the speed of the game to default.                                          |
| Save Position         | Saves your coordinates within the current map.                                    |
| Restore Position      | Teleports you to the set of previously saved coordinates within the current map.  |
| Teleport Forward      | Teleports you a short distance forward (including through objects).               |
| Toggle World Freeze   | Halts the game, while still allowing you to move around freely.                   |
| Toggle HUD            | Enables/Disables the HUD overlay.                                                 |
| Toggle Damage Numbers | Enables/Disables damage numbers being displayed when damaging enemies.            |
| Toggle Third Person   | Switches between first person and third person camera modes.                      |
| Quit Without Saving   | Leave the current game session without saving, reverting to the last saved state. |