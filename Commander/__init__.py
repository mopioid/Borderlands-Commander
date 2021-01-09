from unrealsdk import *
from Mods import ModMenu

from typing import List
import math
from fractions import Fraction


def _GetPlayerController():
	"""Return the current WillowPlayerController object for the local player."""
	return GetEngine().GamePlayers[0].Actor


_DefaultGameInfo = FindObject("WillowCoopGameInfo", "WillowGame.Default__WillowCoopGameInfo")
"""A reference to the WillowCoopGameInfo template object."""
# We use this for managing game speed, as transient WorldInfo objects pull
# their TimeDilation from it.


def _Feedback(feedback):
	"""Presents a "training" message to the user with the given string."""

	# Get the current player controller and the graphics object for its HUD.
	playerController = _GetPlayerController()
	HUDMovie = playerController.GetHUDMovie()

	# If there is no graphics object, we cannot display feedback.
	if HUDMovie is None:
		return

	# We will be displaying the message for two *real time* seconds.
	duration = 2.0 * _DefaultGameInfo.GameSpeed
	# Clear any previous message that may be displayed.
	HUDMovie.ClearTrainingText()
	# Present the training message as per the method's signature:
	#     AddTrainingText(string MessageString, string TitleString, float Duration, Color DrawColor, string HUDInitializationFrame, bool PausesGame, float PauseContinueDelay, PlayerReplicationInfo Related_PRI1, optional bool bIsntActuallyATrainingMessage, optional WillowPlayerController.EBackButtonScreen StatusMenuTab, optional bool bMandatory)
	HUDMovie.AddTrainingText(feedback, "Commander", duration, (), "", False, 0, playerController.PlayerReplicationInfo, True)

def _ToggleThirdPerson():
	playerController = _GetPlayerController()
	# Check the state of the current player controller's camera. If it is
	# in third person, we will be switching to first, and vice versa.
	camera = "ThirdPerson" if playerController.UsingFirstPersonCamera() else "FirstPerson"
	playerController.SetCameraMode(camera)

def _HalveGameSpeed():
	speed = _DefaultGameInfo.GameSpeed
	if speed > 0.0625:
		speed /= 2
		worldInfo = GetEngine().GetCurrentWorldInfo()
		worldInfo.TimeDilation = speed
		_DefaultGameInfo.GameSpeed = speed
	_Feedback("Game Speed: " + str(Fraction(speed)))

def _DoubleGameSpeed():
	speed = _DefaultGameInfo.GameSpeed
	if speed < 32:
		speed *= 2
		worldInfo = GetEngine().GetCurrentWorldInfo()
		worldInfo.TimeDilation = speed
		_DefaultGameInfo.GameSpeed = speed
	_Feedback("Game Speed: " + str(Fraction(speed)))

def _ResetGameSpeed():
	worldInfo = GetEngine().GetCurrentWorldInfo()
	worldInfo.TimeDilation = 1.0
	_DefaultGameInfo.GameSpeed = 1.0
	_Feedback("Game Speed: 1")

def _ToggleHUD():
	_GetPlayerController().myHUD.ToggleHUD()

# For toggling damage numbers, we locate the particle system object resposible
# for emitting them.
_DamageNumberParticleSystem = FindObject("ParticleSystem", "FX_CHAR_Damage_Matrix.Particles.Part_Dynamic_Number")
# The SDK cannot currently replace individual FArray members with nulls, so we
# create two of our own copies of its emitter array; one that emits damage
# numbers, and one that doesn't.
_DamageNumberEmitters = list(_DamageNumberParticleSystem.Emitters)
_NoDamageNumberEmitters = list(_DamageNumberParticleSystem.Emitters)
# The first two particles in the emitter array are the ones responsible for
# damage numbers, so we replace them with nulls in the "no damage number" array.
_NoDamageNumberEmitters[0] = None
_NoDamageNumberEmitters[1] = None

def _ToggleDamageNumbers():
	if _ModInstance.DamageNumbers.CurrentValue:
		_DamageNumberEmitterObject.Emitters = _NoDamageNumberEmitters
		_Feedback("Damage Numbers: Off")
	else:
		_DamageNumberEmitterObject.Emitters = _DamageNumberEmitters
		_Feedback("Damage Numbers: On")

	_ModInstance.DamageNumbers.CurrentValue = not _ModInstance.DamageNumbers.CurrentValue
	ModMenu.SaveModSettings(_ModInstance)


def _GetMapName():
	return GetEngine().GetCurrentWorldInfo().GetMapName(True)

def _GetRotationAndLocation():
	# Assume our local player controller is the first in the engine's list.
	playerController = _GetPlayerController()
	# Our rotation struct is stored in the player controller, while our
	# location struct is stored in its associated pawn object.
	return playerController.Rotation, playerController.Pawn.Location

def _SavePosition():
	rotation, location = _GetRotationAndLocation()
	position = { "X": location.X, "Y": location.Y, "Z": location.Z, "Pitch": rotation.Pitch, "Yaw": rotation.Yaw }

	_ModInstance.Positions.CurrentValue[_GetMapName()] = position
	ModMenu.SaveModSettings(_ModInstance)

	_Feedback("Saved Position")

def _RestorePosition():
	mapName = _GetMapName()
	if mapName in _ModInstance.Positions.CurrentValue:
		position = _ModInstance.Positions.CurrentValue[mapName]

		rotation, location = _GetRotationAndLocation()
		location.X = position["X"]
		location.Y = position["Y"]
		location.Z = position["Z"]
		rotation.Pitch = position["Pitch"]
		rotation.Yaw = position["Yaw"]

		_Feedback("Restored Position")
	else:
		_Feedback("No Position Saved")

_RadiansConversion = 65535.0 / math.pi / 2.0

def _MoveForward():
	rotation, location = _GetRotationAndLocation()

	pitch = rotation.Pitch / _RadiansConversion
	yaw = rotation.Yaw / _RadiansConversion

	location.Z += math.sin(pitch) * 250
	location.X += math.cos(yaw) * math.cos(pitch) * 250
	location.Y += math.sin(yaw) * math.cos(pitch) * 250

def _TogglePlayersOnly():
	# Get the current WorldInfo object from the engine.
	worldInfo = GetEngine().GetCurrentWorldInfo()
	# Get the WorldInfo's current players only state.
	playersOnly = worldInfo.bPlayersOnly

	# Display the state we will be switching to to the user.
	_Feedback("Players Only: " + ("Off" if playersOnly else "On"))
	# Apply the change.
	worldInfo.bPlayersOnly = not playersOnly

def _QuitWithoutSaving():
	_GetPlayerController().ConsoleCommand("disconnect", False)


_KeybindActions = {
	"Halve Game Speed":      _HalveGameSpeed,
	"Double Game Speed":     _DoubleGameSpeed,
	"Reset Game Speed":      _ResetGameSpeed,
	"Save Position":         _SavePosition,
	"Restore Position":      _RestorePosition,
	"Teleport Forward":      _MoveForward,
	"Toggle World Freeze":   _TogglePlayersOnly,
	"Toggle HUD":            _ToggleHUD,
	"Toggle Damage Numbers": _ToggleDamageNumbers,
	"Toggle Third Person":   _ToggleThirdPerson,
	"Quit Without Saving":   _QuitWithoutSaving,
}


class Commander(ModMenu.SDKMod):
	Name: str = "Commander"
	Version: str = "2.0"
	Description: str = "Perform various changes to the game using key bindings."
	Author: str = "mopioid"
	Types: ModTypes = ModTypes.Gameplay

	SaveEnabledState: ModMenu.EnabledSaveType = ModMenu.EnabledSaveType.LoadWithSettings

	Keybinds: List[ModMenu.Keybind] = [
		ModMenu.Keybind( "Halve Game Speed",      "LeftBracket"  ),
		ModMenu.Keybind( "Double Game Speed",     "RightBracket" ),
		ModMenu.Keybind( "Reset Game Speed",      "Backslash"    ),
		ModMenu.Keybind( "Save Position",         "Period"       ),
		ModMenu.Keybind( "Restore Position",      "Comma"        ),
		ModMenu.Keybind( "Teleport Forward",      "Up"           ),
		ModMenu.Keybind( "Toggle World Freeze",   "Slash"        ),
		ModMenu.Keybind( "Toggle HUD",            "Semicolon"    ),
		ModMenu.Keybind( "Toggle Damage Numbers", "Quote"        ),
		ModMenu.Keybind( "Toggle Third Person",   "Equals"       ),
		ModMenu.Keybind( "Quit Without Saving",   "End"          ),
	]

	Positions: ModMenu.Options.Hidden = ModMenu.Options.Hidden("Positions", StartingValue={})
	DamageNumbers: ModMenu.Options.Hidden = ModMenu.Options.Hidden("DamageNumbers", StartingValue=True)
	Options: List[ModMenu.Options.Base] = [Positions, DamageNumbers]

	def __init__(self):
		ModMenu.LoadModSettings(self)
		if not self.DamageNumbers.CurrentValue:
			_DamageNumberEmitterObject.Emitters = _NoDamageNumberEmitters

	def GameInputPressed(self, input):
		if input.Name in _KeybindActions:
			_KeybindActions[input.Name]()

Mods.append(Commander())
