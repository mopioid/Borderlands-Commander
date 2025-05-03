from . import _game

from mods_base import BaseOption, BoolOption
from mods_base.keybinds import (
    keybind,
    Block,
    EInputEvent,
    KeybindBlockSignal,
    KeybindType,
)

try:
    import networking  # pyright: ignore[reportMissingImports]
except ImportError:
    networking = None

from fractions import Fraction
from time import time_ns


options: list[BaseOption] = []


if networking:
    _client_speed = BoolOption(
        identifier="Client Speed Permissions",
        value=False,
        description=(
            "Should clients in multiplayer be allowed to modify the speed of"
            " the game."
        ),
    )

    options.append(_client_speed)

    @networking.host.json_message
    def _server_request_game_speed(speed: float) -> None:
        if _client_speed.value:
            _broadcast_game_speed(speed)
        else:
            player = _server_request_game_speed.sender
            _client_popup(player, f"Only session host may modify game speed")

    @networking.host.json_message
    def _server_request_game_freeze(should_freeze: bool) -> None:
        if _client_speed.value:
            _broadcast_game_freeze(should_freeze)
        else:
            player = _server_request_game_speed.sender
            _client_popup(player, f"Only session host may toggle game freeze")

    @networking.broadcast.json_message
    def _broadcast_game_speed(speed: float) -> None:
        _game.set_speed(speed)
        _game.popup(f"Game speed: {Fraction(speed)}")

    @networking.broadcast.json_message
    def _broadcast_game_freeze(should_freeze: bool) -> None:
        _game.set_freeze(should_freeze)
        message = "On" if should_freeze else "Off"
        _game.popup(f"World Freeze: {message}")

    @networking.targeted.string_message
    def _client_popup(message: str) -> None:
        _game.popup(message)

    def set_speed(speed: float) -> None:
        if _game.is_client():
            _server_request_game_speed(speed)
        else:
            _broadcast_game_speed(speed)

    def toggle_freeze() -> None:
        should_freeze = not _game.get_freeze()

        if _game.is_client():
            _server_request_game_freeze(should_freeze)
        else:
            _broadcast_game_freeze(should_freeze)

else:

    def set_speed(speed: float) -> None:
        _game.set_speed(speed)
        _game.popup(f"Game speed: {Fraction(speed)}")

    def toggle_freeze() -> None:
        should_freeze = not _game.get_freeze()

        _game.set_freeze(should_freeze)
        message = "On" if should_freeze else "Off"
        _game.popup(f"World Freeze: {message}")


speed_held = False
speed_direction: bool | None = None
last_scroll = 0


@keybind(
    identifier="Change Game Speed",
    description=(
        "In game, hold and scroll up with the mousewheel to increase game"
        " speed. Hold and scroll down with the mousewheel to decrease game"
        " speed. Hold and click with the mousewheel to freeze time."
    ),
    key="Backslash",
    event_filter=None,
)
def _speed_key_callback(event: EInputEvent) -> KeybindBlockSignal:
    global speed_held, speed_direction

    if event == EInputEvent.IE_Pressed:
        speed_held = True
        speed = _game.get_speed()
        speed_direction = None if speed == 1 else (speed > 1)

    elif event == EInputEvent.IE_Released:
        speed_held = False


@keybind(
    identifier="Increase Game Speed",
    key="MouseScrollUp",
    is_hidden=True,
    is_rebindable=False,
    event_filter=None,
)
def _speedup_callback(event: EInputEvent) -> KeybindBlockSignal:
    global last_scroll, speed_direction

    if not speed_held or time_ns() < last_scroll + 50_000000:
        return

    last_scroll = time_ns()

    if event == EInputEvent.IE_Pressed:
        speed = _game.get_speed()
        if speed == 0:
            return

        if speed_direction == None:
            speed_direction = True

        elif speed_direction == False and speed == 1:
            return

        if speed < 32.0:
            speed *= 2
            set_speed(speed)

    return Block


@keybind(
    identifier="Decrease Game Speed",
    key="MouseScrollDown",
    is_hidden=True,
    is_rebindable=False,
    event_filter=None,
)
def _speeddown_callback(event: EInputEvent) -> KeybindBlockSignal:
    global last_scroll, speed_direction

    if not speed_held or time_ns() < last_scroll + 50_000000:
        return

    last_scroll = time_ns()

    if event == EInputEvent.IE_Pressed:
        speed = _game.get_speed()
        if speed == 0:
            return

        if speed_direction == None:
            speed_direction = False

        elif speed_direction == True and speed == 1:
            return

        if speed > (1.0 / 32.0):
            speed /= 2.0
            set_speed(speed)

    return Block


@keybind(
    identifier="World Freeze",
    key="MiddleMouseButton",
    is_hidden=True,
    is_rebindable=False,
    event_filter=None,
)
def _worldfreeze_callback(event: EInputEvent) -> KeybindBlockSignal:
    if not speed_held:
        return

    if event == EInputEvent.IE_Pressed:
        toggle_freeze()

    return Block


keybinds: list[KeybindType] = [
    _speed_key_callback,
    _speedup_callback,
    _speeddown_callback,
    _worldfreeze_callback,
]
