from ._positions import (
    Position,
    saved_positions,
    client_positions,
    spawn_positions,
)
from ._game import popup, dialog, console_command

__all__ = (
    "Position",
    "saved_positions",
    "client_positions",
    "spawn_positions",
    "popup",
    "dialog",
    "console_command",
)


from . import _game, _positions, _speed, _custom

import mods_base

try:
    from networking import NetworkFunction
except ImportError:
    NetworkFunction = None

from itertools import chain

from typing import Any, Protocol, Sequence


class CommanderModule(Protocol):
    options: list[mods_base.BaseOption]
    keybinds: list[mods_base.KeybindType]


modules: Sequence[CommanderModule] = (_positions, _speed, _custom)


class Commander(mods_base.Mod):
    should_enable = False
    enable_guard = False

    def load_settings(self) -> None:
        _custom.load_keybinds()

        self.options = tuple(
            chain.from_iterable(module.options for module in modules)
        )
        self.keybinds = tuple(
            chain.from_iterable(module.keybinds for module in modules)
        )

        self.enable_guard = True

        super().load_settings()

        if _custom._legacy_commands.value:
            _custom.import_legacy()
            self.keybinds = tuple(
                chain.from_iterable(module.keybinds for module in modules)
            )
            super().load_settings()

        if _custom._legacy_commands in _custom.options:
            _custom.options.remove(_custom._legacy_commands)
        self.options = tuple(
            chain.from_iterable(module.options for module in modules)
        )

        legacy_positions_dict: dict[str, list[dict[str, Any] | None]] = (
            _positions._positions_dict.value  # pyright: ignore[reportAssignmentType]
        )
        ported_positions_dict: dict[str, dict[str, dict[str, Any]]] = dict()

        for (
            map_name,
            legacy_map_positions,
        ) in legacy_positions_dict.items():
            if not isinstance(
                legacy_map_positions, list
            ):  # pyright: ignore[reportUnnecessaryIsInstance]
                break

            ported_map_positions = ported_positions_dict.setdefault(
                map_name, dict()
            )
            for index, legacy_position in enumerate(legacy_map_positions):
                if not legacy_position:
                    continue

                ported_position: dict[str, Any] = dict()
                for key, value in legacy_position.items():
                    ported_position[key.lower()] = value

                ported_map_positions[str(index + 1)] = ported_position
                if not index:
                    ported_map_positions["10"] = ported_position

        if ported_positions_dict:
            _positions._positions_dict.value = ported_positions_dict  # pyright: ignore[reportAttributeAccessIssue]

        self.enable_guard = False
        if self.should_enable:
            self.enable()

    def enable(self) -> None:
        self.should_enable = True
        if self.enable_guard:
            return

        for module in modules:
            for key, value in vars(module).items():
                if NetworkFunction and isinstance(value, NetworkFunction):
                    value.enable()
                elif key == "on_enable":
                    value()

        super().enable()

    def disable(self, dont_update_setting: bool = False) -> None:
        for module in modules:
            for key, value in vars(module).items():
                if NetworkFunction and isinstance(value, NetworkFunction):
                    value.disable()
                elif key == "on_disable":
                    value()

        super().disable(dont_update_setting)


_game.mod = mods_base.build_mod(cls=Commander)
