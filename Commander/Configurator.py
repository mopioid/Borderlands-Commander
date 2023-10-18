from Mods import ModMenu, UserFeedback #type: ignore
from Mods.ModMenu import SettingsManager #type: ignore

from . import Commander, Builtin


class CustomConfigurator(UserFeedback.OptionBox):
    def __init__(self):
        buttons = []
        for name in Commander.CustomCommands.CurrentValue:
            if Builtin.KeybindExists(name):
                continue
            buttons.append(UserFeedback.OptionBoxButton(name))

        if not len(buttons):
            buttons = [UserFeedback.OptionBoxButton("Create new…")]

        super().__init__(
            Title="Commander Custom Console Commands",
            Caption="Modify the list of custom console commands you would like Commander to be able to execute.",
            Tooltip="[Enter] Edit    [Delete] Delete    [N] Create New    [Escape] Exit",
            Buttons=buttons,
        )
        self.Show()

    def OnInput(self, key: str, event: int) -> None:
        if key == "N" and event == 1:
            self.Hide()
            _CustomCreatorName()
        elif key in ("Delete", "BackSpace") and event == 1 and len(Commander.CustomCommands.CurrentValue):
            name = self.GetSelectedButton().Name
            self.Hide()
            _CustomDeleter(name)

    def OnPress(self, button: UserFeedback.OptionBoxButton) -> None:
        if len(Commander.CustomCommands.CurrentValue):
            _CustomEditorName(button.Name)
        else:
            _CustomCreatorName()


class _CustomDeleter(UserFeedback.OptionBox):
    def __init__(self, name: str):
        super().__init__(
            Title=f"Delete '{name}'?",
            Caption="This cannot be undone.",
            Buttons=[UserFeedback.OptionBoxButton("Yes"), UserFeedback.OptionBoxButton("No")],
        )
        self._custom_command_name = name
        self.Show()

    def OnPress(self, button: UserFeedback.OptionBoxButton) -> None:
        if button.Name == "Yes":
            del Commander.CustomCommands.CurrentValue[self._custom_command_name]
            keybind = Commander.Instance.CustomKeybindForName(self._custom_command_name)
            Commander.Instance.Keybinds.remove(keybind)
            SettingsManager.SaveModSettings(Commander.Instance)

        CustomConfigurator()

    def OnCancel(self) -> None:
        CustomConfigurator()


class _CustomCreatorName(UserFeedback.TextInputBox):
    def __init__(self, name = ""):
        super().__init__(Title="Enter Nickname for New Console Command", DefaultMessage=name)
        self.Show()

    def OnSubmit(self, name: str) -> None:
        if name == "":
            CustomConfigurator()
        elif name in Commander.CustomCommands.CurrentValue:
            _CustomCreatorOverwrite(name)
        elif Builtin.KeybindExists(name):
            _CustomCreatorConflict(name)
        else:
            _CustomCreatorCommand(name)

class _CustomCreatorOverwrite(UserFeedback.OptionBox):
    def __init__(self, name: str):
        super().__init__(
            Title="Command Already Exists",
            Caption=f"A custom console command with the nickname '{name}' already exists. Would you like to override it?",
            Buttons=[UserFeedback.OptionBoxButton("Yes"), UserFeedback.OptionBoxButton("No")],
        )
        self._custom_command_name = name
        self.Show()

    def OnPress(self, button: UserFeedback.OptionBoxButton) -> None:
        if button.Name == "Yes":
            _CustomCreatorCommand(self._custom_command_name)
        if button.Name == "No":
            _CustomCreatorName(self._custom_command_name)

    def OnCancel(self) -> None:
        _CustomCreatorName(self._custom_command_name)

class _CustomCreatorConflict(UserFeedback.TrainingBox):
    def __init__(self, name: str):
        super().__init__(
            Title="Invalid Nickname",
            Message=f"A built-in Commander feature with the nickname '{name}' already exists, please choose another name.",
        )
        self._custom_command_name = name
        self.Show()

    def OnExit(self) -> None:
        _CustomCreatorName(self._custom_command_name)

class _CustomCreatorCommand(UserFeedback.TextInputBox):
    def __init__(self, name: str, command: str = ""):
        super().__init__(
            Title=f"Enter Console Command for '{name}'",
            DefaultMessage=command
        )
        self._custom_command_name = name
        self.Show()

    def OnSubmit(self, command: str) -> None:
        if command == "":
            _CustomCreatorName(self._custom_command_name)
        else:
            Commander.CustomCommands.CurrentValue[self._custom_command_name] = command

            try:
                on_press = Commander.CompileCustomCommand(command)
            except Exception as exception:
                _CustomCreatorError(self._custom_command_name, command, exception)
                return

            keybind = Commander.Instance.CustomKeybindForName(self._custom_command_name)
            if keybind:
                keybind.OnPress = on_press
            else:
                keybind = ModMenu.Keybind(self._custom_command_name, OnPress=on_press)
                Commander.Instance.Keybinds.append(keybind)
                SettingsManager.SaveModSettings(Commander.Instance)

            CustomConfigurator()

class _CustomCreatorError(UserFeedback.TrainingBox):
    def __init__(self, name: str, command: str, exception: Exception):
        super().__init__(Title="Custom Command Error", Message=Commander.FormatCommandException(exception))
        self._custom_command_name = name
        self._custom_command = command
        self.Show()

    def OnExit(self) -> None:
        _CustomCreatorCommand(self._custom_command_name, self._custom_command)


class _CustomEditorName(UserFeedback.TextInputBox):
    def __init__(self, old_name, new_name = None):
        if not new_name:
            new_name = old_name
        super().__init__(Title=f"Enter new Nickname for '{old_name}'", DefaultMessage=new_name)
        self._old_custom_command_name = old_name
        self.Show()

    def OnSubmit(self, new_name: str) -> None:
        if new_name == "":
            CustomConfigurator()
        elif new_name == self._old_custom_command_name:
            _CustomEditorCommand(new_name)
        elif new_name in Commander.CustomCommands.CurrentValue:
            _CustomEditorOverwrite(self._old_custom_command_name, new_name)
        elif Builtin.KeybindExists(new_name):
            _CustomEditorConflict(self._old_custom_command_name, new_name)
        else:
            Commander.CustomCommands.CurrentValue[new_name] = Commander.CustomCommands.CurrentValue[self._old_custom_command_name]
            del Commander.CustomCommands.CurrentValue[self._old_custom_command_name]

            keybind = Commander.Instance.CustomKeybindForName(self._old_custom_command_name)
            keybind.Name = new_name

            _CustomEditorCommand(new_name)

class _CustomEditorOverwrite(UserFeedback.OptionBox):
    def __init__(self, old_name: str, new_name: str):
        super().__init__(
            Title="Command Already Exists",
            Caption=f"A custom console command with the nickname '{new_name}' already exists. Would you like to override it?",
            Buttons=[UserFeedback.OptionBoxButton("Yes"), UserFeedback.OptionBoxButton("No")],
        )
        self._old_custom_command_name = old_name
        self._new_custom_command_name = new_name
        self.Show()

    def OnPress(self, button: UserFeedback.OptionBoxButton) -> None:
        if button.Name == "Yes":
            kept_command = Commander.CustomCommands.CurrentValue[self._old_custom_command_name]
            Commander.CustomCommands.CurrentValue[self._new_custom_command_name] = kept_command
            del Commander.CustomCommands.CurrentValue[self._old_custom_command_name]

            kept_keybind = Commander.Instance.CustomKeybindForName(self._old_custom_command_name)
            kept_keybind.Name = self._new_custom_command_name

            replaced_keybind = Commander.Instance.CustomKeybindForName(self._new_custom_command_name)
            Commander.Instance.Keybinds.remove(replaced_keybind)
            SettingsManager.SaveModSettings(Commander.Instance)

            _CustomEditorCommand(self._new_custom_command_name)

        if button.Name == "No":
            _CustomEditorName(self._old_custom_command_name)

    def OnCancel(self) -> None:
        _CustomEditorName(self._old_custom_command_name)

class _CustomEditorConflict(UserFeedback.TrainingBox):
    def __init__(self, old_name: str, new_name: str):
        super().__init__(
            Title="Invalid Nickname",
            Message=f"A built-in Commander feature with the nickname '{new_name}' already exists, please choose another name.",
        )
        self._custom_command_old_name = old_name
        self._custom_command_new_name = new_name
        self.Show()

    def OnExit(self) -> None:
        _CustomEditorName(self._custom_command_old_name, self._custom_command_new_name)

class _CustomEditorCommand(UserFeedback.TextInputBox):
    def __init__(self, name: str, command: str = None):
        if not command:
            command = Commander.CustomCommands.CurrentValue[name]
        super().__init__(Title=f"Edit Console Command for '{name}'", DefaultMessage=command)
        self._custom_command_name = name
        self.Show()

    def OnSubmit(self, command: str) -> None:
        if command == "":
            _CustomEditorName(self._custom_command_name)
        elif command == self._custom_command_name:
            CustomConfigurator()
        else:
            try:
                on_press = Commander.CompileCustomCommand(command)
            except Exception as exception:
                _CustomEditorError(self._custom_command_name, command, exception)
                return

            Commander.CustomCommands.CurrentValue[self._custom_command_name] = command

            keybind = Commander.Instance.CustomKeybindForName(self._custom_command_name)
            if keybind:
                keybind.OnPress = on_press
            else:
                keybind = ModMenu.Keybind(self._custom_command_name, OnPress=on_press)
                Commander.Instance.Keybinds.append(keybind)

            SettingsManager.SaveModSettings(Commander.Instance)
            CustomConfigurator()

class _CustomEditorError(UserFeedback.TrainingBox):
    def __init__(self, name: str, command: str, exception: Exception):
        super().__init__(Title="Custom Command Error", Message=Commander.FormatCommandException(exception))
        self._custom_command_name = name
        self._custom_command = command
        self.Show()

    def OnExit(self) -> None:
        _CustomEditorCommand(self._custom_command_name, self._custom_command)
