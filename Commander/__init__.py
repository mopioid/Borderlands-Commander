from unrealsdk import *
from Mods import ModMenu

from Mods.ModMenu import ServerMethod, ClientMethod

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
# We use this for managing game speed, as WorldInfo objects pull their TimeDilation from it.


def _Feedback(feedback):
    """Presents a "training" message to the user with the given string."""
    PC = _GetPlayerController()

    # Get the graphics object for our player controller's HUD.
    HUDMovie = PC.GetHUDMovie()

    # If there is no graphics object, we cannot display feedback.
    if HUDMovie is None:
        return

    # We will be displaying the message for two *real time* seconds.
    duration = 2.0 * _DefaultGameInfo.GameSpeed
    # Clear any previous message that may be displayed.
    HUDMovie.ClearTrainingText()
    # Present the training message as per the method's signature:
    #     AddTrainingText(string MessageString, string TitleString, float Duration, Color DrawColor, string HUDInitializationFrame, bool PausesGame, float PauseContinueDelay, PlayerReplicationInfo Related_PRI1, optional bool bIsntActuallyATrainingMessage, optional WillowPlayerController.EBackButtonScreen StatusMenuTab, optional bool bMandatory)
    HUDMovie.AddTrainingText(feedback, "Commander", duration, (), "", False, 0, PC.PlayerReplicationInfo, True)


def _ToggleThirdPerson():
    PC = _GetPlayerController()
    PC.SetBehindView(not PC.bBehindView)


def _ApplyGameSpeed(speed):
    GetEngine().GetCurrentWorldInfo().TimeDilation = _DefaultGameInfo.GameSpeed = speed
    _Feedback("Game Speed: " + str(Fraction(speed)))
    _ModInstance.ClientApplyGameSpeed(speed)

def _HalveGameSpeed():
    speed = _DefaultGameInfo.GameSpeed
    if speed > 0.0625:
        speed /= 2
        if _IsClient():
            _ModInstance.ServerRequestGameSpeed(speed)
        else:
            _ApplyGameSpeed(speed)

def _DoubleGameSpeed():
    speed = _DefaultGameInfo.GameSpeed
    if speed < 32:
        speed *= 2
        if _IsClient():
            _ModInstance.ServerRequestGameSpeed(speed)
        else:
            _ApplyGameSpeed(speed)

def _ResetGameSpeed():
    speed = _DefaultGameInfo.GameSpeed
    if speed != 1.0:
        speed = 1.0
        if _IsClient():
            _ModInstance.ServerRequestGameSpeed(speed)
        else:
            _ApplyGameSpeed(speed)
    else:
        _Feedback("Game Speed: 1")


# For toggling damage numbers, we locate the particle system object resposible for emitting them.
_DamageNumberParticleSystem = FindObject("ParticleSystem", "FX_CHAR_Damage_Matrix.Particles.Part_Dynamic_Number")
# The SDK cannot currently replace individual FArray members with nulls, so we create two of our own
# copies of its emitter array; one that emits damage numbers, and one that doesn't.
_DamageNumberEmitters = list(_DamageNumberParticleSystem.Emitters)
_NoDamageNumberEmitters = list(_DamageNumberParticleSystem.Emitters)
# The first two particles in the emitter array are the ones responsible for damage numbers, so we
# replace them with nulls in the "no damage number" array.
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

def _GetVehicle(PC):
    _, vehicle = PC.IsUsingVehicleEx(True)
    return None if vehicle is None else vehicle.GetPawnToTeleport()

def _GetPosition(PC):
    location = PC.Pawn.Location
    rotation = PC.Rotation
    return {
        "X": location.X, "Y": location.Y, "Z": location.Z,
        "Pitch": rotation.Pitch, "Yaw": rotation.Yaw
    }

def _ApplyPosition(PC, position):
    location = position["X"], position["Y"], position["Z"]
    rotation = position["Pitch"], position["Yaw"], 0

    _, vehicle = PC.IsUsingVehicleEx(True)
    if vehicle is None:
        PC.NoFailSetPawnLocation(PC.Pawn, location)
    else:
        pawn = vehicle.GetPawnToTeleport()
        pawn.Mesh.SetRBPosition(location);
        pawn.Mesh.SetRBRotation(rotation);
    PC.ClientSetRotation(rotation)

def _SavePosition():
    mapName = _GetMapName()

    positions = _Positions.CurrentValue.get(mapName, [None, None, None])
    positions[_Position] = _GetPosition(_GetPlayerController())

    _Positions.CurrentValue[mapName] = positions
    ModMenu.SaveModSettings(_ModInstance)

    _Feedback(f"Saved Position {_Position + 1}")

def _RestorePosition():
    PC = _GetPlayerController()
    position = _Positions.CurrentValue.get(_GetMapName(), [None, None, None])[_Position]
    if position is None:
        _Feedback(f"Position {_Position + 1} Not Saved")

    elif _IsClient():
        _ModInstance.ServerRequestPosition(position, name=str(_Position + 1))

    else:
        _ApplyPosition(PC, position)
        _Feedback(f"Restored Position {_Position + 1}")

        if _ClientTeleporting.CurrentValue == "With Host":
            for PRI in GetEngine().GetCurrentWorldInfo().GRI.PRIArray:
                if PRI.Owner is not None:
                    _ApplyPosition(PRI.Owner, position)
            _ModInstance.ClientApplyPosition(position, name="")

def _MoveForward():
    PC = _GetPlayerController()
    position = _GetPosition(PC)

    # Convert our pitch and yaw from the game's units to radians.
    pitch = position["Pitch"] / 65535 * math.tau
    yaw   = position["Yaw"  ] / 65535 * math.tau

    position["Z"] += math.sin(pitch) * 250
    position["X"] += math.cos(yaw) * math.cos(pitch) * 250
    position["Y"] += math.sin(yaw) * math.cos(pitch) * 250

    if _IsClient():
        _ModInstance.ServerRequestPosition(position, name=None)
    else:
        _ApplyPosition(PC, position)


def _ApplyPlayersOnly(playersOnly):
    GetEngine().GetCurrentWorldInfo().bPlayersOnly = playersOnly
    _Feedback("World Freeze: " + ("On" if playersOnly else "Off"))
    _ModInstance.ClientApplyPlayersOnly(playersOnly)

def _TogglePlayersOnly():
    playersOnly = not GetEngine().GetCurrentWorldInfo().bPlayersOnly
    if _IsClient():
        _ModInstance.ServerRequestPlayersOnly(playersOnly)
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
    Choices=["Allow", "With Host", "None"],
    StartingValue="Allow"
)
_ClientSpeedPermissions = ModMenu.Options.Boolean(
    Caption="Client Speed Permissions",
    Description="Should clients in multiplayer be allowed to modify the speed of the game.",
    StartingValue=False
)


class Commander(ModMenu.SDKMod):
    Name: str = "Commander"
    Version: str = "2.1"
    Description: str = "Perform various changes to the game using key bindings."
    Author: str = "mopioid"
    Types: ModTypes = ModTypes.Gameplay

    Options: List[ModMenu.Options.Base] = [
        _Positions, _DamageNumbers, _ClientTeleporting, _ClientSpeedPermissions
    ]
    SaveEnabledState: ModMenu.EnabledSaveType = ModMenu.EnabledSaveType.LoadWithSettings

    Keybinds: List[ModMenu.Keybind] = [
        ModMenu.Keybind( "Toggle Third Person",   "Equals",       OnPress=_ToggleThirdPerson   ),
        ModMenu.Keybind( "Halve Game Speed",      "LeftBracket",  OnPress=_HalveGameSpeed      ),
        ModMenu.Keybind( "Double Game Speed",     "RightBracket", OnPress=_DoubleGameSpeed     ),
        ModMenu.Keybind( "Reset Game Speed",      "None",         OnPress=_ResetGameSpeed      ),
        ModMenu.Keybind( "Toggle World Freeze",   "Backslash",    OnPress=_TogglePlayersOnly   ),
        ModMenu.Keybind( "Toggle HUD",            "Semicolon",    OnPress=_ToggleHUD           ),
        ModMenu.Keybind( "Toggle Damage Numbers", "Quote",        OnPress=_ToggleDamageNumbers ),
        ModMenu.Keybind( "Save Position",         "Period",       OnPress=_SavePosition        ),
        ModMenu.Keybind( "Restore Position",      "Comma",        OnPress=_RestorePosition     ),
        ModMenu.Keybind( "Select Position",       "Slash",        OnPress=_SelectPosition      ),
        ModMenu.Keybind( "Teleport Forward",      "Up",           OnPress=_MoveForward         ),
        ModMenu.Keybind( "Quit Without Saving",   "End",          OnPress=_QuitWithoutSaving   ),
    ]
    
    def Enable(self):
        super().Enable()
        if not _DamageNumbers.CurrentValue:
            _DamageNumberParticleSystem.Emitters = _NoDamageNumberEmitters

    def Disable(self):
        super().Disable()
        _DamageNumberParticleSystem.Emitters = _DamageNumberEmitters

    @ClientMethod
    def ClientApplyGameSpeed(self, speed, PC = None):
        _ApplyGameSpeed(speed)

    @ClientMethod
    def ClientApplyPlayersOnly(self, playersOnly, PC = None):
        _ApplyPlayersOnly(playersOnly)

    @ClientMethod
    def ClientApplyPosition(self, position, name, PC = None):
        _ApplyPosition(_GetPlayerController(), position)
        if name is not None:
            _Feedback(f"Restored Position " + name)

    @ClientMethod
    def ClientFeedback(self, feedback, PC = None):
        _Feedback(feedback)

    @ServerMethod
    def ServerRequestPosition(self, position, name, PC = None):
        if _ClientTeleporting.CurrentValue == "Allow":
            _ApplyPosition(PC, position)
            self.ClientApplyPosition(position, name, PC)
        else:
            self.ClientFeedback("Only session host may teleport players.", PC)

    @ServerMethod
    def ServerRequestGameSpeed(self, speed, PC = None):
        if _ClientSpeedPermissions.CurrentValue:
            _ApplyGameSpeed(speed)
        else:
            self.ClientFeedback("Only session host may modify game speed.", PC)

    @ServerMethod
    def ServerRequestPlayersOnly(self, playersOnly, PC = None):
        if _ClientSpeedPermissions.CurrentValue:
            _ApplyPlayersOnly(playersOnly)
        else:
            self.ClientFeedback("Only session host may toggle game freeze.", PC)


_ModInstance = Commander()
ModMenu.RegisterMod(_ModInstance)

for mapName, positions in _Positions.CurrentValue.items():
    if type(positions) is dict:
        _Positions.CurrentValue[mapName] = [positions, None, None]
    else:
        break
ModMenu.SaveModSettings(_ModInstance)
