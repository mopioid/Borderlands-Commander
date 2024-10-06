from unrealsdk import Log, GetEngine, RunHook, RemoveHook, UObject, UFunction, FStruct #type: ignore

from Mods import ModMenu, __file__ as _ModsPath #type: ignore
from Mods.ModMenu import ClientMethod, ServerMethod, SettingsManager #type: ignore

import os, webbrowser
from typing import Any, Callable, Dict, List, Optional, Tuple

from . import Builtin
try:
    from Mods import UserFeedback #type: ignore
    from . import Configurator
except:
    Configurator = None


_Main: Dict[str, Any] = vars(__import__("__main__"))

exec("""
from unrealsdk import *
from Mods.Commander.Builtin import PC, Popup
""", _Main)


class _CommanderConfiguratorButton(ModMenu.Options.Field):
    def __init__(self) -> None:
        self.Caption = "Custom Commands"
        self.Description = (
            "Enter the configurator for custom console commands executable by Commander."
            "<!-- hey gurl heyyy ;) -->"
        )
        self.IsHidden = False

ConfiguratorButton = _CommanderConfiguratorButton()

CustomCommands = ModMenu.Options.Hidden(
    Caption="CustomCommands",
    StartingValue={
        "Toggle HUD": "py PC().myHUD.ToggleHUD()",
        "Toggle Third Person": "py PC().SetBehindView(not PC().bBehindView)",
        "Quit Without Saving": "py PC().ReturnToTitleScreen(True, False)",
        "Respawn Enemies": "set PopulationOpportunityDen bIsWaitingForRespawn True|set PopulationOpportunityDen RespawnDelayStartTime -10000",
    }
)


def FormatCommandException(exception: Exception) -> str:
    if not isinstance(exception, SyntaxError):
        return exception.__repr__()
    return f"{exception.msg} at line {exception.lineno} column {exception.offset}:\n{exception.text}"

def CompileCustomCommand(command: str) -> Callable[[], None]:
    if command.startswith("py "):
        code = compile(command[3:], "<string>", "exec")
        return lambda: exec(code, _Main)
    elif command.startswith("pyexec "):
        filename = os.path.join(os.path.dirname(_ModsPath), command[7:])
        return lambda: exec(open(filename).read(), _Main)
    else:
        return lambda: Builtin.PC().ConsoleCommand(command)


class Commander(ModMenu.SDKMod):
    Name: str = "Commander"
    Version: str = "2.6"
    Description: str = "Perform various actions in game using key bindings."
    Author: str = "mopioid"
    Types: ModMenu.ModTypes = ModMenu.ModTypes.Gameplay
    SaveEnabledState: ModMenu.EnabledSaveType = ModMenu.EnabledSaveType.LoadWithSettings

    Options: Tuple[ModMenu.Options.Base] = (ConfiguratorButton, CustomCommands) + Builtin.Options
    Keybinds: List[ModMenu.Keybind] = list(Builtin.Keybinds)

    _performed_init: bool = False

    def __init__(self):
        super().__init__()
        SettingsManager.LoadModSettings(self)

        for map_name, positions in Builtin.Positions.CurrentValue.items():
            if type(positions) is dict:
                Builtin.Positions.CurrentValue[map_name] = [positions, None, None]
            else:
                break

        for name, command in CustomCommands.CurrentValue.items():
            try:
                on_press = CompileCustomCommand(command)
                self.Keybinds.append(ModMenu.Keybind(name, OnPress=on_press))
            except Exception as exception:
                Log(f"Commander: Cannot register custom command '{name}': {FormatCommandException(exception)}")

        SettingsManager.LoadModSettings(self)
        self._performed_init = True


    def CustomKeybindForName(self, name: str) -> Optional[ModMenu.Keybind]:
        for keybind in self.Keybinds[len(Builtin.Keybinds):]:
            if keybind.Name == name:
                return keybind
        return None


    @property
    def IsEnabled(self) -> bool:
        if self._is_enabled is None:
            return self.Status == "Enabled"
        return self._is_enabled

    @IsEnabled.setter
    def IsEnabled(self, val: bool) -> None:
        self._is_enabled = val
        if self._performed_init and self.SaveEnabledState != ModMenu.EnabledSaveType.NotSaved:
            SettingsManager.SaveModSettings(self)

    def Enable(self):
        super().Enable()
        if not Builtin.DamageNumbers.CurrentValue:
            Builtin.DamageNumberParticleSystem.Emitters = Builtin.NoDamageNumberEmitters

        RunHook("WillowGame.WillowScrollingList.OnClikEvent", "Commander", WillowScrollingListOnClikEvent)

    def Disable(self):
        super().Disable()
        Builtin.DamageNumberParticleSystem.Emitters = Builtin.DamageNumberEmitters

        RemoveHook("WillowGame.WillowScrollingList.OnClikEvent", "Commander")


    @ClientMethod
    def ClientApplyGameSpeed(self, speed, PC = None):
        Builtin.ApplyGameSpeed(speed)

    @ClientMethod
    def ClientApplyPlayersOnly(self, playersOnly, PC = None):
        Builtin.ApplyPlayersOnly(playersOnly)

    @ClientMethod
    def ClientApplyPosition(self, position, name, PC = None):
        Builtin.ApplyPosition(GetEngine().GamePlayers[0].Actor, position)
        if name is not None:
            Builtin.Feedback(f"Restored Position " + name)

    @ClientMethod
    def ClientFeedback(self, feedback, PC = None):
        Builtin.Feedback(feedback)

    @ServerMethod
    def ServerRequestPosition(self, position, name, PC = None):
        if Builtin.ClientTeleporting.CurrentValue == "Allow":
            Builtin.ApplyPosition(PC, position)
            self.ClientApplyPosition(position, name, PC)
        else:
            self.ClientFeedback("Only session host may teleport players.", PC)

    @ServerMethod
    def ServerRequestGameSpeed(self, speed, PC = None):
        if Builtin.ClientSpeedPermissions.CurrentValue:
            Builtin.ApplyGameSpeed(speed)
        else:
            self.ClientFeedback("Only session host may modify game speed.", PC)

    @ServerMethod
    def ServerRequestPlayersOnly(self, playersOnly, PC = None):
        if Builtin.ClientSpeedPermissions.CurrentValue:
            Builtin.ApplyPlayersOnly(playersOnly)
        else:
            self.ClientFeedback("Only session host may toggle game freeze.", PC)


def WillowScrollingListOnClikEvent(caller: UObject, function: UFunction, params: FStruct) -> bool:
    """
    Copied from ModMenu.OptionManager to detect clicking of menu items, modified to detect
    the description of our configurator "button."
    """
    if params.Data.Type != "itemClick":
        return True

    provider = None
    for obj in caller.DataProviderStack:
        provider = obj.DataProvider.ObjectPointer
    if provider is None or provider.GetDescription is None:
        return True

    event_id = caller.IndexToEventId[params.Data.Index]
    event_description = provider.GetDescription(event_id)
    if event_description == ConfiguratorButton.Description:
        if Configurator:
            Configurator.CustomConfigurator()
        else:
            webbrowser.open("https://github.com/mopioid/Borderlands-Commander/wiki/Custom-Commands")

    return True


Instance: Commander = Commander()
