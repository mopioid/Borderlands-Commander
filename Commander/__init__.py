from unrealsdk import *
from Mods import ModMenu

from Mods.ModMenu import ServerMethod
from Mods.ModMenu import ClientMethod

from typing import List
import math
from fractions import Fraction


def _GetPlayerController():
	return GetEngine().GamePlayers[0].Actor

def _GetMapName():
	return GetEngine().GetCurrentWorldInfo().GetMapName(True)

def _IsClient():
	return GetEngine().GetCurrentWorldInfo().NetMode == 3


_DefaultGameInfo = FindObject("WillowCoopGameInfo", "WillowGame.Default__WillowCoopGameInfo")
"""A reference to the WillowCoopGameInfo template object."""
# We use this for managing game speed, as transient WorldInfo objects pull
# their TimeDilation from it.


def _Feedback(feedback):
	"""Presents a "training" message to the user with the given string."""
	playerController = _GetPlayerController()

	# Get the graphics object for our player controller's HUD.
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
	playerController.SetBehindView(not playerController.bBehindView)


def _ApplyGameSpeed(speed):
	GetEngine().GetCurrentWorldInfo().TimeDilation = _DefaultGameInfo.GameSpeed = speed
	_Feedback("Game Speed: " + str(Fraction(speed)))
	_ModInstance.ClientApplyGameSpeed(None, speed)

def _HalveGameSpeed():
	speed = _DefaultGameInfo.GameSpeed
	if speed > 0.0625:
		speed /= 2
		if _IsClient():
			_ModInstance.ServerRequestGameSpeed(None, speed)
		else:
			_ApplyGameSpeed(speed)

def _DoubleGameSpeed():
	speed = _DefaultGameInfo.GameSpeed
	if speed < 32:
		speed *= 2
		if _IsClient():
			_ModInstance.ServerRequestGameSpeed(None, speed)
		else:
			_ApplyGameSpeed(speed)

def _ResetGameSpeed():
	speed = _DefaultGameInfo.GameSpeed
	if speed != 1.0:
		speed = 1.0
		if _IsClient():
			_ModInstance.ServerRequestGameSpeed(None, speed)
		else:
			_ApplyGameSpeed(speed)
	else:
		_Feedback("Game Speed: 1")


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
	_DamageNumbers.CurrentValue = not _DamageNumbers.CurrentValue
	ModMenu.SaveModSettings(_ModInstance)

	CallPostEdit(False)
	if _DamageNumbers.CurrentValue:
		_DamageNumberParticleSystem.Emitters = _DamageNumberEmitters
		_Feedback("Damage Numbers: On")
	else:
		_DamageNumberParticleSystem.Emitters = _NoDamageNumberEmitters
		_Feedback("Damage Numbers: Off")
	CallPostEdit(True)


_Position = 0

def _SelectPosition():
	global _Position
	if   _Position == 0:
		 _Position =  1
	elif _Position == 1:
		 _Position =  2
	elif _Position == 2:
		 _Position =  0
	_Feedback(f"Selected Position {_Position + 1}")

def _GetPosition(playerController):
	location = playerController.Pawn.Location
	rotation = playerController.Rotation
	return {
		"X": location.X, "Y": location.Y, "Z": location.Z,
		"Pitch": rotation.Pitch, "Yaw": rotation.Yaw
	}

def _ApplyPosition(playerController, position):
	location = playerController.Pawn.Location
	location.X, location.Y, location.Z = position["X"], position["Y"], position["Z"]
	rotation = playerController.Rotation
	rotation.Pitch, rotation.Yaw = position["Pitch"], position["Yaw"]

def _SavePosition():
	mapName = _GetMapName()

	positions = _Positions.CurrentValue.get(mapName, [None, None, None])
	positions[_Position] = _GetPosition(_GetPlayerController())

	_Positions.CurrentValue[mapName] = positions
	ModMenu.SaveModSettings(_ModInstance)

	_Feedback(f"Saved Position {_Position + 1}")

def _RestorePosition():
	playerController = _GetPlayerController()
	position = _Positions.CurrentValue.get(_GetMapName(), [None, None, None])[_Position]
	if position is None:
		_Feedback(f"Position {_Position + 1} Not Saved")

	elif _IsClient():
		_ModInstance.ServerRequestPosition(None, position, str(_Position + 1))

	else:
		_ApplyPosition(playerController, position)
		_Feedback(f"Restored Position {_Position + 1}")

		if _ClientTeleporting.CurrentValue == "With Host":
			for PRI in GetEngine().GetCurrentWorldInfo().GRI.PRIArray:
				if PRI.Owner is not None:
					_ApplyPosition(PRI.Owner, position)
			_ModInstance.ClientApplyPosition(None, position, "")


def _MoveForward():
	playerController = _GetPlayerController()
	position = _GetPosition(playerController)

	# Convert our pitch and yaw from the game's units to radians.
	pitch = position["Pitch"] / 65535 * math.tau
	yaw   = position["Yaw"  ] / 65535 * math.tau

	position["Z"] += math.sin(pitch) * 250
	position["X"] += math.cos(yaw) * math.cos(pitch) * 250
	position["Y"] += math.sin(yaw) * math.cos(pitch) * 250

	if _IsClient():
		_ModInstance.ServerRequestPosition(None, position, None)
	else:
		_ApplyPosition(playerController, position)


def _ApplyPlayersOnly(playersOnly):
	GetEngine().GetCurrentWorldInfo().bPlayersOnly = playersOnly
	_Feedback("World Freeze: " + ("On" if playersOnly else "Off"))
	_ModInstance.ClientApplyPlayersOnly(None, playersOnly)

def _TogglePlayersOnly():
	playersOnly = not GetEngine().GetCurrentWorldInfo().bPlayersOnly
	if _IsClient():
		_ModInstance.ServerRequestPlayersOnly(None, playersOnly)
	else:
		_ApplyPlayersOnly(playersOnly)


def _ToggleHUD():
	_GetPlayerController().myHUD.ToggleHUD()

def _QuitWithoutSaving():
	_GetPlayerController().ConsoleCommand("disconnect", False)


_Positions = ModMenu.Options.Hidden(
	Caption="Positions",
	StartingValue={}
)
_DamageNumbers = ModMenu.Options.Hidden(
	Caption="DamageNumbers",
	StartingValue=True
)
_ClientTeleporting = ModMenu.Options.Spinner(
	Caption="Client Teleporting",
	Description="Should clients in multiplayer be allowed to teleport their location, or should their location be teleported with the host.",
	StartingValue="Allow",
	Choices=["Allow", "With Host", "None"]
)
_ClientSpeedPermissions = ModMenu.Options.Boolean(
	Caption="Client Speed Permissions",
	Description="Should clients in multiplayer be allowed to modify the speed of the game.",
	StartingValue=False
)


def _Keybind(name, key, function):
	keybind = ModMenu.Keybind(name, key)
	keybind.Function = function
	return keybind


class Commander(ModMenu.SDKMod):
	Name: str = "Commander"
	Version: str = "2.1"
	Description: str = "Perform various changes to the game using key bindings."
	Author: str = "mopioid"
	Types: ModTypes = ModTypes.Gameplay

	SaveEnabledState: ModMenu.EnabledSaveType = ModMenu.EnabledSaveType.LoadWithSettings
	Options: List[ModMenu.Options.Base] = [
		_Positions, _DamageNumbers, _ClientTeleporting, _ClientSpeedPermissions
	]

	Keybinds: List[ModMenu.Keybind] = [
		_Keybind( "Toggle Third Person",   "Equals",       _ToggleThirdPerson   ),
		_Keybind( "Halve Game Speed",      "LeftBracket",  _HalveGameSpeed      ),
		_Keybind( "Double Game Speed",     "RightBracket", _DoubleGameSpeed     ),
		_Keybind( "Reset Game Speed",      "None",         _ResetGameSpeed      ),
		_Keybind( "Toggle World Freeze",   "Backslash",    _TogglePlayersOnly   ),
		_Keybind( "Toggle HUD",            "Semicolon",    _ToggleHUD           ),
		_Keybind( "Toggle Damage Numbers", "Quote",        _ToggleDamageNumbers ),
		_Keybind( "Save Position",         "Period",       _SavePosition        ),
		_Keybind( "Restore Position",      "Comma",        _RestorePosition     ),
		_Keybind( "Select Position",       "Slash",        _SelectPosition      ),
		_Keybind( "Teleport Forward",      "Up",           _MoveForward         ),
		_Keybind( "Quit Without Saving",   "End",          _QuitWithoutSaving   ),
	]
	
	def GameInputPressed(self, bind):
		bind.Function()

	def Enable(self):
		super().Enable()
		if not _DamageNumbers.CurrentValue:
			_DamageNumberParticleSystem.Emitters = _NoDamageNumberEmitters

	def Disable(self):
		super().Disable()
		_DamageNumberParticleSystem.Emitters = _DamageNumberEmitters

	@ClientMethod
	def ClientApplyGameSpeed(self, caller, speed):
		_ApplyGameSpeed(speed)

	@ClientMethod
	def ClientApplyPlayersOnly(self, caller, playersOnly):
		_ApplyPlayersOnly(playersOnly)

	@ClientMethod
	def ClientApplyPosition(self, caller, position, name):
		_ApplyPosition(_GetPlayerController(), position)
		if name is not None:
			_Feedback(f"Restored Position " + name)

	@ClientMethod
	def ClientFeedback(self, caller, feedback):
		_Feedback(feedback)

	@ServerMethod
	def ServerRequestPosition(self, caller, position, name):
		if _ClientTeleporting.CurrentValue == "Allow":
			_ApplyPosition(caller, position)
			self.ClientApplyPosition(caller, position, name)
		else:
			self.ClientFeedback(caller, "Only session host may teleport players.")

	@ServerMethod
	def ServerRequestGameSpeed(self, caller, speed):
		if _ClientSpeedPermissions.CurrentValue:
			_ApplyGameSpeed(speed)
		else:
			self.ClientFeedback(caller, "Only session host may modify game speed.")

	@ServerMethod
	def ServerRequestPlayersOnly(self, caller, playersOnly):
		if _ClientSpeedPermissions.CurrentValue:
			_ApplyPlayersOnly(playersOnly)
		else:
			self.ClientFeedback(caller, "Only session host may toggle game freeze.")


_ModInstance = Commander()
ModMenu.RegisterMod(_ModInstance)

for mapName, positions in _Positions.CurrentValue.items():
	if type(positions) is dict:
		_Positions.CurrentValue[mapName] = [positions, None, None]
	else:
		break
ModMenu.SaveModSettings(_ModInstance)
