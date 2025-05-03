from __future__ import annotations

from . import _game

from unrealsdk import make_struct
from unrealsdk.unreal import UObject, WrappedStruct
from mods_base.keybinds import (
    keybind,
    Block,
    EInputEvent,
    KeybindBlockSignal,
    KeybindType,
)
from mods_base import BaseOption, HiddenOption, BoolOption, get_pc

try:
    import networking
except ImportError:
    networking = None

import dataclasses
import math

from typing import Iterator, Self, Sequence, TypedDict, overload
from types import EllipsisType


@dataclasses.dataclass
class Position:
    x: float = 0.0
    """The Position's X coordinate"""
    y: float = 0.0
    """The Position's Y coordinate"""
    z: float = 0.0
    """The Position's Z coordinate"""
    pitch: _game.Angle = _game.Angle(0)
    """The Position's pitch (up and down) angle, in the game's units"""
    yaw: _game.Angle = _game.Angle(0)
    """The Position's yaw (left and right) angle, in the game's units"""

    @property
    def pitch_radians(self) -> float:
        """The Position's pitch (up and down) angle, in radians"""
        return _game.to_radians(self.pitch)

    @pitch_radians.setter
    def pitch_radians(self, radians: float) -> None:
        self.pitch = _game.from_radians(radians)

    @property
    def yaw_radians(self) -> float:
        """The Position's yaw (left and right) angle, in radians"""
        return _game.to_radians(self.yaw)

    @yaw_radians.setter
    def yaw_radians(self, radians: float) -> None:
        self.yaw = _game.from_radians(radians)

    @classmethod
    def _fromdict(cls, position_dict: PositionDict) -> Self:
        return cls(**position_dict)

    def _asdict(self) -> PositionDict:
        return dataclasses.asdict(self)  # pyright: ignore[reportReturnType]

    @classmethod
    def from_player_pc(cls, player_pc: UObject | EllipsisType = ...) -> Self:
        """
        Create a Position object from the player's current position
        Args:
            player_pc:
                If specified, the PlayerController object from which to get the
                position
        Returns: The Position object
        """
        if isinstance(player_pc, EllipsisType):
            player_pc = get_pc()
        return _game.get_player_pc_position(cls, player_pc)

    @classmethod
    def from_structs(
        cls, vector: WrappedStruct, rotator: WrappedStruct | None = None
    ) -> Self:
        """
        Create a Position object from a Vector and (optionally) Rotator struct
        Args:
            vector: The Vector struct to use for X, Y, and Z coordinates
            rotator:
                If specified, the Rotator struct to use for pitch and yaw
                angles
        Returns: The Position object
        """
        return (
            cls(
                vector.X,
                vector.Y,
                vector.Z,
                rotator.Pitch,
                rotator.Yaw,
            )
            if rotator
            else cls(vector.X, vector.Y, vector.Z)
        )

    @classmethod
    def from_actor(cls, actor: UObject) -> Self:
        """
        Create a Position object from the Actor UObject.
        Args:
            actor: The Actor UObject from which to get the position.
        Returns: The Position object
        """
        return _game.get_actor_position(cls, actor)

    def teleport_player_pc(
        self, player_pc: UObject | EllipsisType = ...
    ) -> None:
        """
        Teleport the player to this position.

        If teleporting the local player when they are a client in the network
        game, the teleportation is requested from the host.
        Args:
            player_pc:
                If specified, the PlayerController object to teleport,
                otherwise the local player's controller is used.
        """
        if isinstance(player_pc, EllipsisType) or player_pc == get_pc():
            _teleport_position(self, None)
        else:
            _game.set_player_pc_position(self, player_pc)

    def teleport_actor(self, actor: UObject) -> None:
        """
        Teleport the specified Actor UObject to this position.

        Attempting to teleport an Actor when a client in a network game will
        fail under most circumstances.
        Args:
            actor: The Actor UObject to teleport.
        """
        _game.set_actor_position(self, actor)

    def shift_forward(self, distance: float) -> None:
        """
        Modify this Position object by shifting its coordinates "forward"
        according to its pitch and yaw
        Args:
            distance: The distance in game units to shift the position by
        """
        pitch = _game.to_radians(self.pitch)
        yaw = _game.to_radians(self.yaw)

        self.z += math.sin(pitch) * distance
        self.x += math.cos(yaw) * math.cos(pitch) * distance
        self.y += math.sin(yaw) * math.cos(pitch) * distance

    def distance(self, other: Position | None = None) -> float:
        """
        Calculate the distance between this Position object and another
        Args:
            other:
                If specified, the other Position object to calculate distance
                from. Otherwise, the origin (0, 0, 0) is used.
        """
        if not other:
            other = _origin_position

        return math.sqrt(
            (self.x - other.x) ** 2
            + (self.y - other.y) ** 2
            + (self.z - other.z) ** 2
        )

    def make_vector(self) -> WrappedStruct:
        """
        Create a Vector struct with this Position's X, Y, and Z coordinates.
        """
        return make_struct("Vector", X=self.x, Y=self.y, Z=self.z)

    def make_rotator(self) -> WrappedStruct:
        """
        Create a Rotator struct with this Position's pitch and yaw angles.
        """
        return make_struct("Rotator", Pitch=self.pitch, Yaw=self.yaw)


_origin_position = Position()


class CommanderPositions(Sequence[Position | None]):
    def __len__(self) -> int:
        return 11

    def __iter__(self) -> Iterator[Position | None]:
        map_positions_dict = _positions_dict.value.get(_game.get_map(), {})
        for index in range(len(self)):
            position_dict = map_positions_dict.get(str(index))
            yield (
                Position._fromdict(position_dict) if position_dict else None
            )

    @overload
    def __getitem__(self, index: int) -> Position | None: ...

    @overload
    def __getitem__(self, index: slice) -> Sequence[Position | None]: ...

    def __getitem__(
        self, index: int | slice
    ) -> Position | None | Sequence[Position | None]:
        indices = range(len(self))[index]

        map_positions_dict = _positions_dict.value.get(_game.get_map(), {})

        if isinstance(indices, int):
            position_dict = map_positions_dict.get(str(indices))
            return Position._fromdict(position_dict) if position_dict else None

        return tuple(
            (
                Position._fromdict(map_positions_dict[str(index)])
                if str(index) in map_positions_dict
                else None
            )
            for index in indices
        )

    def __setitem__(self, index: int, value: Position | None) -> None:
        map_name = _game.get_map()
        map_positions_dict = _positions_dict.value.get(map_name)
        if map_positions_dict is None:
            map_positions_dict = {}
            _positions_dict.value[map_name] = map_positions_dict

        if value:
            map_positions_dict[str(index)] = value._asdict()
        else:
            del map_positions_dict[str(index)]

        _game.mod.save_settings()


saved_positions = CommanderPositions()
"""
A sequence Position objects representing the player's saved positions for the
map in which they are currently playing.

This sequence will always be of length 11. Each index corresponds to the
position saved with the keyboard key for that number. Index 10 representes the
the position saved without pressing an additional keyboard key.

Accessing elements of this sequence will always provide update-to-date
information as the map changes or as the player saves new positions.

In addition, assigning elements of this sequence will also modify the player's
saved positions.
"""


class SpawnPositions(Sequence[Position]):

    def __len__(self) -> int:
        _update_map_spawns()
        return _map_spawn_count

    def __iter__(self) -> Iterator[Position]:
        _update_map_spawns()
        return iter(_map_spawns)

    @overload
    def __getitem__(self, index: int) -> Position: ...

    @overload
    def __getitem__(self, index: slice) -> Sequence[Position]: ...

    def __getitem__(self, index: int | slice) -> Position | Sequence[Position]:
        _update_map_spawns()
        return _map_spawns[index]


spawn_positions = SpawnPositions()
"""
A sequence of Position objects representing the spawn points in the map in
which the player is currently playing.

Accessing elements of this sequence will always provide update-to-date
information as the map changes.

This sequence will always contain the same positions in the same order for a
given map (barring effects of any mods that alter spawn points).
"""


class ClientPositions(Sequence[Position]):
    def __len__(self) -> int:
        return 0 if _game.is_client() else len(_game.get_players()) - 1

    def __iter__(self) -> Iterator[Position]:
        for player in _game.get_players():
            player_pc = _game.get_player_pc(player)
            if player_pc and player_pc != get_pc():
                yield _game.get_player_pc_position(Position, player_pc)

    @overload
    def __getitem__(self, index: int) -> Position: ...

    @overload
    def __getitem__(self, index: slice) -> Sequence[Position]: ...

    def __getitem__(self, index: int | slice) -> Position | Sequence[Position]:
        return tuple(self)[index]


client_positions = ClientPositions()
"""
A sequence of Position objects representing the positions of the others players
in a co-op session.

This sequence is only functional when the host in a co-op session; for client
players, it will be empty.
"""


class PositionDict(TypedDict):
    x: float
    y: float
    z: float
    pitch: _game.Angle
    yaw: _game.Angle


_positions_dict = HiddenOption[
    dict[
        str, dict[str, PositionDict]
    ]  # pyright: ignore[reportInvalidTypeArguments]
]("Positions", dict())

options: list[BaseOption] = [_positions_dict]


_map_name = ""

_map_spawns: list[Position]
_map_spawn_count = 0
_next_spawn_index = 0

_save_held = False
_restore_held = False
_spawn_held = False
_forward_held = False
_num_pressed = False


def _player_at_index(index: int) -> UObject | None:
    player_index = 0
    for player in _game.get_players():
        if _game.get_player_pc(player) == get_pc():
            continue
        if index == player_index:
            return player
        player_index += 1


def _filter_position(position: Position) -> bool:
    for spawn in _map_spawns:
        if position.distance(spawn) < 4000:
            return False
    return True


def _update_map_spawns() -> None:
    global _next_spawn_index, _map_name, _map_spawns, _map_spawn_count

    new_map_name = _game.get_map()
    if new_map_name == _map_name:
        return

    _map_name = new_map_name
    _next_spawn_index = 0

    if _game.is_client():
        _map_spawn_count = 1
        return

    _map_spawns = []

    for positions in _game.get_spawns():
        _map_spawns += list(
            sorted(
                filter(_filter_position, positions),
                key=Position.distance,
            )
        )

    _map_spawn_count = len(_map_spawns)


if networking:
    _client_teleporting = BoolOption(
        identifier="Client Teleporting",
        value=True,
        true_text="Allow",
        false_text="Disallow",
        description=(
            "Should clients in multiplayer be allowed to teleport their"
            " position."
        ),
    )
    options.append(_client_teleporting)

    @networking.targeted.string_message
    def _client_popup(message: str) -> None:
        _game.popup(message)

    @networking.host.json_message
    def _server_reqest_position(
        position_dict: PositionDict, message: str | None
    ) -> None:
        client = _server_reqest_position.sender

        if not _client_teleporting.value:
            _client_popup(client, "Only game host may teleport players.")
            return

        client_pc = _game.get_player_pc(client)
        if not client_pc:
            raise

        _game.set_player_pc_position(
            Position._fromdict(position_dict),
            client_pc,
        )
        if message:
            _client_popup(client, message)

    def _teleport_position(position: Position, message: str | None) -> None:
        if _game.is_client():
            _server_reqest_position(
                position._asdict(),
                message,
            )

        else:
            _game.set_player_pc_position(position, get_pc())
            if message:
                _game.popup(message)

    @networking.targeted.json_message
    def _client_spawn_info(count: int, message: str | None) -> None:
        global _map_spawn_count
        _map_spawn_count = count
        if message:
            _game.popup(message)

    @networking.host.json_message
    def _server_reqest_spawn(index: int) -> None:
        client = _server_reqest_spawn.sender

        if not _client_teleporting.value:
            _client_popup(client, "Only game host may teleport players.")
            return

        _update_map_spawns()

        if index >= _map_spawn_count:
            index = 0

        client_pc = _game.get_player_pc(client)
        if not client_pc:
            raise

        _game.set_player_pc_position(_map_spawns[index], client_pc)
        _client_spawn_info(
            client, _map_spawn_count, f"Teleported to Spawn {index + 1}"
        )

    def _teleport_spawn(index: int) -> None:
        if _game.is_client():
            _server_reqest_spawn(index)
        else:
            _teleport_position(
                _map_spawns[index], f"Teleported to Spawn {index + 1}"
            )

    @networking.host.json_message
    def _server_request_player(target_player_id: int) -> None:
        client = _server_request_player.sender

        if not _client_teleporting.value:
            _client_popup(client, "Only game host may teleport players.")
            return

        for target_player in _game.get_players():
            if _game.get_player_id(target_player) == target_player_id:
                break
        else:
            raise Exception(f"Client requested non-existant PlayerID")

        target_pc = _game.get_player_pc(target_player)
        if not target_pc:
            raise

        target_name = _game.get_player_name(target_player)
        target_position = _game.get_player_pc_position(Position, target_pc)

        client_pc = _game.get_player_pc(client)
        if not client_pc:
            raise

        _game.set_player_pc_position(target_position, client_pc)
        _client_popup(client, f"Teleported to {target_name}")

    def _teleport_player(index: int) -> None:
        target_player = _player_at_index(index)
        if not target_player:
            return

        if _game.is_client():
            target_player_id = _game.get_player_id(target_player)
            _server_request_player(target_player_id)
        else:
            target_pc = _game.get_player_pc(target_player)
            if not target_pc:
                raise

            target_name = _game.get_player_name(target_player)
            target_position = _game.get_player_pc_position(Position, target_pc)
            _teleport_position(target_position, f"Teleported to {target_name}")

else:

    def _teleport_position(position: Position, message: str | None) -> None:
        _game.set_player_pc_position(position, get_pc())
        if message:
            _game.popup(message)

    def _teleport_spawn(index: int) -> None:
        _teleport_position(
            _map_spawns[index], f"Teleported to Spawn {index + 1}"
        )

    def _teleport_player(index: int) -> None:
        target_player = _player_at_index(index)
        if not target_player:
            return

        target_pc = _game.get_player_pc(target_player)
        if not target_pc:
            return

        target_name = _game.get_player_name(target_player)
        target_position = _game.get_player_pc_position(Position, target_pc)
        _teleport_position(target_position, f"Teleported to {target_name}")


@keybind(
    identifier="Save Position",
    key="Period",
    description=(
        "In game, tap to save your current position. Hold and press a number"
        " key to save a position for that number."
    ),
    event_filter=None,
)
def save_keybind(event: EInputEvent) -> KeybindBlockSignal:
    global _save_held, _num_pressed

    if event == EInputEvent.IE_Pressed:
        _save_held = True

    elif event == EInputEvent.IE_Released:
        if not _num_pressed:
            saved_positions[10] = Position.from_player_pc()
            _game.popup(f"Saved Position")

        _save_held = False
        if not (_spawn_held or _restore_held):
            _num_pressed = False


@keybind(
    identifier="Restore Position",
    key="Comma",
    description=(
        "In game, tap this key to save your current position. Hold and press a"
        " number key to save a position for that number."
    ),
    event_filter=None,
)
def restore_keybind(event: EInputEvent) -> KeybindBlockSignal:
    global _restore_held, _num_pressed

    if event == EInputEvent.IE_Pressed:
        _restore_held = True

    elif event == EInputEvent.IE_Released:
        if not _num_pressed:
            if position := saved_positions[10]:
                _teleport_position(position, "Restored Position")
            else:
                _game.popup(f"Position Not Saved")

        _restore_held = False
        if not (_spawn_held or _save_held):
            _num_pressed = False


@keybind(
    identifier="Teleport to Spawn",
    description=(
        "In game, tap to teleport to your saved position. Hold and press a"
        " number key to teleport to your saved position for that number."
    ),
    key="Slash",
    event_filter=None,
)
def spawn_keybind(event: EInputEvent) -> KeybindBlockSignal:
    global _spawn_held, _num_pressed, _next_spawn_index

    if event == EInputEvent.IE_Pressed:
        _spawn_held = True

    elif event == EInputEvent.IE_Released:
        if not _num_pressed:
            _update_map_spawns()
            if _next_spawn_index >= _map_spawn_count:
                _next_spawn_index = 0

            _teleport_spawn(_next_spawn_index)
            _next_spawn_index += 1

        _spawn_held = False
        if not (_restore_held or _save_held):
            _num_pressed = False


@keybind(
    identifier="Teleport Forward",
    description=(
        "In game, tap to teleport forward a short distance. Hold and press a"
        " number key to teleport forward further distances."
    ),
    key="Up",
    event_filter=None,
)
def forward_keybind(event: EInputEvent) -> KeybindBlockSignal:
    global _forward_held, _num_pressed

    if event == EInputEvent.IE_Pressed:
        _forward_held = True

    elif event == EInputEvent.IE_Released:
        if not _num_pressed:
            position = Position.from_player_pc()
            position.shift_forward(250)
            _teleport_position(position, None)

        _forward_held = False
        _num_pressed = False


keybinds: list[KeybindType] = [
    save_keybind,
    restore_keybind,
    spawn_keybind,
    forward_keybind,
]

for index, key in enumerate(
    (
        "Zero",
        "One",
        "Two",
        "Three",
        "Four",
        "Five",
        "Six",
        "Seven",
        "Eight",
        "Nine",
    )
):

    def callback(
        event: EInputEvent,
        index: int = index,
        shifted_index: int = index - 1 if index else 9,
        forward_distance: int = 250 * (index + 1 if index else 11),
    ) -> KeybindBlockSignal:
        global _num_pressed, _next_spawn_index

        if not (_save_held or _restore_held or _spawn_held or _forward_held):
            return

        if event == EInputEvent.IE_Pressed:
            _num_pressed = True

            if _restore_held and _spawn_held:
                _teleport_player(shifted_index)

            elif _save_held:
                saved_positions[index] = Position.from_player_pc()
                _game.popup(f"Saved Position {index}")

            elif _restore_held:
                if position := saved_positions[index]:
                    _teleport_position(position, f"Restored Position {index}")
                else:
                    _game.popup(f"Position {index} Not Saved")

            elif _spawn_held:
                _update_map_spawns()
                if shifted_index < _map_spawn_count:
                    _teleport_spawn(shifted_index)
                    _next_spawn_index = shifted_index + 1

            elif _forward_held:
                position = Position.from_player_pc()
                position.shift_forward(forward_distance)
                _teleport_position(position, None)

        return Block

    for key in (key, "NumPad" + key):
        keybinds.append(
            keybind(
                identifier=key,
                key=key,
                callback=callback,
                is_hidden=True,
                is_rebindable=False,
                event_filter=None,
            )
        )
