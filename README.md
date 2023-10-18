# Borderlands Commander
An [UnrealEngine PythonSDK](https://github.com/bl-sdk/PythonSDK) mod for Borderlands 2 and Borderlands: The Pre-Sequel! that provides useful functionality while in-game:
* Configuring your own hotkeys to run console commands of your choice.
* Saving and teleporting your position in the world.
* Freezing time.
* Modifying game speed.
* Quitting without saving.
* Toggling HUD elements.
* Toggling Third Person camera.

See the video below for a brief demonstration.

[![Borderlands Commander Intro](https://i.imgur.com/ZY1nw1z.jpg)](https://youtu.be/ftfeGFUteWI)

This is almost entirely made possible thanks to the work of the UnrealEngine PythonSDK team. Special thanks to LightChaosman and his [NoDamageNumbers mod](https://github.com/BLCM/BLCMods/blob/master/Borderlands%202%20mods/LightChaosman/NoDamageNumbers.txt), FromDarkHell for various modding tidbits, JoltzDude139 for expert testing and feedback, and c0dycode for originally making Commander possible via [CommandInjector](https://github.com/c0dycode/BL-CommandInjector).

## Installation

See: [Installing Borderlands Commander](https://github.com/mopioid/Borderlands-Commander/wiki/Installation).

## Usage

The built-in features of Borderlands Commander are operated using key inputs during gameplay. These key bindings may be configured in game via OPTIONS > KEYBOARD/MOUSE > MODDED KEY BINDINGS:

| Action                | Description                                                                       |
|-----------------------|-----------------------------------------------------------------------------------|
| Halve Game Speed      | Decreases the speed of the game to 1/2, then 1/4, etc., to a minimum of 1/32      |
| Double Game Speed     | Increases the speed of the game to x2, then x4, etc., to a maximum of x32         |
| Reset Game Speed      | Resets the speed of the game to default.                                          |
| Toggle World Freeze   | Halts the game, while still allowing you to move around freely.                   |
| Toggle Damage Numbers | Enables/Disables damage numbers being displayed when damaging enemies.            |
| Save Position         | Saves your position to the selected slot for the current map.                     |
| Restore Position      | Teleports you to the position saved to the selected slot for the current map.     |
| Select Position       | Selects the next slot for saving and restoring positions in the current map.      |
| Teleport Forward      | Teleports you a short distance forward (including through objects).               |

In addition, Borderlands Commander allows you to create hotkeys for your own custom console commands. See: [Custom Commands in Borderlands Commander](https://github.com/mopioid/Borderlands-Commander/wiki/Custom-Commands). Included with Commander are four default commands:

| Action                | Description                                                                       |
|-----------------------|-----------------------------------------------------------------------------------|
| Toggle HUD            | Enables/Disables the HUD overlay.                                                 |
| Toggle Third Person   | Switches between first person and third person camera modes.                      |
| Quit Without Saving   | Leave the current game session without saving, reverting to the last saved state. |
| Respawn Enemies       | Allow nearly every enemy in a map to respawn immediately.                         |

Borderlands Commander also has two options that can be configured under OPTIONS > MODS:

| Option                         | Description                                                                                                   |
|--------------------------------|---------------------------------------------------------------------------------------------------------------|
| Custom Commands                | Launch the configurator for adding and modifying your own custom console commands.                            |
| Client Teleporting - Allow     | Co-op partners who join your game may use Commander to teleport freely (they must also be running Commander). |
| Client Teleporting - With Host | Co-op partners who join your game will be teleported with you whenever you restore your own position.         |
| Client Teleporting - None      | Co-op partners who join your game cannot teleport.                                                            |
| Client Speed Permissions - On  | Co-op partners who join your game can adjust the game speed and freeze the world (affects all players).       |
| Client Speed Permissions - Off | Co-op partners who join your game cannot adjust the game speed or freeze the world.                           |
