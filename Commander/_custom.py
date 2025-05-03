from . import _game
from ._game import popup

from mods_base import (
    get_pc,
    BaseOption,
    ButtonOption,
    HiddenOption,
    KeybindType,
    SETTINGS_DIR,
)

import os

from typing import Any, Callable


COMMANDS_PATH = SETTINGS_DIR / "Commander.txt"

main_globals = __import__("__main__").__dict__

legacy_locals: dict[str, Any] = {
    "PC": get_pc,
    "Popup": popup,
}

exec(
    """\
try:
    from legacy_compat import legacy_compat

    with legacy_compat():
        from unrealsdk import *
except ImportError:
    pass
""",
    legacy_locals,
)


def init_commands_file() -> None:
    if not os.path.exists(COMMANDS_PATH):
        with open(COMMANDS_PATH, "w", encoding="utf-8") as file:
            file.write(_game.default_commands)


@ButtonOption(
    identifier="Edit Custom Commands",
    description="Open the file containing your custom console commands",
)
def _edit_commands_button(button: ButtonOption) -> None:
    init_commands_file()
    os.startfile(COMMANDS_PATH)
    _game.dialog(
        "Your custom commands file has been opened. When you are finished"
        f" modifying it, click {_reload_commands_button.display_name}."
    )


@ButtonOption(
    identifier="Reload Custom Commands",
    description="Reload the file containing your custom console commands",
)
def _reload_commands_button(button: ButtonOption) -> None:
    _game.mod.load_settings()
    _game.dialog(
        "Custom commands reloaded. To be able to modify their keybinds, exit"
        " Commander's settings and re-open them."
    )


_legacy_commands = HiddenOption[dict[str, str]](
    identifier="CustomCommands", value={}
)


options: list[BaseOption] = [
    _edit_commands_button,
    _reload_commands_button,
    _legacy_commands,
]


def on_enable() -> None:
    exec(
        (
            "from unrealsdk import *\n"
            "from unrealsdk.unreal import *\n"
            "from mods_base import *\n"
            "from Commander import *\n"
        ),
        main_globals,
    )


def import_legacy() -> None:
    with open(COMMANDS_PATH, "w", encoding="utf-8") as file:
        for name, command in _legacy_commands.value.items():
            print(name + ":", file=file)

            if command.startswith("py "):
                lines = command.split("\n")
                lines[0] = lines[0].removeprefix("py ")

                print("py with legacy_compat():", file=file)
                for line in lines:
                    if line.strip():
                        print(" " * 4 + line, file=file)
            else:
                print(command, file=file)

            print(file=file)

    load_keybinds()


keybinds: list[KeybindType] = []


class CommandKeybindType(KeybindType):
    def __init__(self, name: str, command: str, legacy: bool = False) -> None:
        if command.startswith("py "):
            code = compile(command[3:], "<string>", "exec")
            if command.startswith("py with legacy_compat():"):
                callback = lambda: exec(code, main_globals, legacy_locals)
            else:
                callback = lambda: exec(code, main_globals)
        else:
            callback = lambda: _game.console_command(command)

        super().__init__(
            identifier=name,
            key=None,
            display_name=name,
            callback=callback,
        )

    def enable(self) -> None:
        if not self.is_enabled:
            super().enable()

    def disable(self) -> None:
        if self.is_enabled:
            super().disable()


def load_keybinds() -> None:
    for keybind in keybinds:
        keybind.disable()
    keybinds.clear()

    execute_state: Callable[[str], None]
    command_name: str
    command_body: str

    def reading_name(line: str) -> None:
        nonlocal execute_state, command_name

        line_parts = line.split(":", maxsplit=1)
        if len(line_parts) < 2:
            return

        command_name = line_parts[0].strip()
        execute_state = reading_body_start
        execute_state(line_parts[1])

    def reading_body_start(line: str) -> None:
        nonlocal execute_state, command_body

        command_body = line.lstrip()
        if command_body.rstrip():
            execute_state = reading_body

    def reading_body(line: str) -> None:
        nonlocal execute_state, command_body

        if line.strip():
            command_body += line

        else:
            keybind = CommandKeybindType(command_name, command_body)
            keybind.enable()
            keybinds.append(keybind)

            execute_state = reading_name

    execute_state = reading_name

    init_commands_file()
    with open(COMMANDS_PATH, "r", encoding="utf-8") as file:
        for line in file:
            execute_state(line)

    execute_state("")
