from unrealsdk import find_all, make_struct, find_class
from unrealsdk.unreal import UObject

from mods_base import ENGINE, get_pc

from math import tau

from .. import _positions

from ui_utils import show_hud_message, show_modal_tutorial_message

from typing import Sequence, Type


Angle = float
type Position = "_positions.Position"
type PlayerState = UObject
type PlayerController = UObject


default_commands = """\
Teleport to Ping:
py Position.from_structs(get_pc().CachedPlayerAlertLocation).teleport_player_pc()

Respawn Enemies:
py for spawner in find_all("SpawnerComponent", False):
    spawner.ResetSpawning()

Reload Map:
py console_command(f"open {ENGINE.GameViewport.World.Name}")

Quit Without Saving:
py ENGINE.GameViewport.World.AuthorityGameMode.ReturnToMainMenuHost()
"""


def ui_dialog(message: str) -> None:
    show_modal_tutorial_message(
        "Commander", message, image_name="TrueVaultHunter"
    )


def popup(message: str) -> None:
    show_hud_message("Commander", message)


def console_command(command: str) -> None:
    get_pc().ServerGbxConsoleCommand(
        make_struct("ReplicatedConsoleCommandContext", CommandAndArgs=command)
    )


def is_client() -> bool:
    return (
        get_pc().PlayerState
        != ENGINE.GameViewport.World.GameState.HostPlayerState
    )


def get_players() -> Sequence[PlayerState]:
    return ENGINE.GameViewport.World.GameState.PlayerArray


def get_player_pc(player: PlayerState) -> PlayerController | None:
    return player.Owner


def get_player_name(player: PlayerState) -> str:
    return player.PlayerName


def get_player_id(player: PlayerState) -> int:
    return player.PlayerId


def to_radians(angle: Angle) -> float:
    return angle / 360 * tau


def from_radians(radians: float) -> Angle:
    return Angle(radians * 360 / tau)


def get_map() -> str:
    return ENGINE.GameViewport.World.Name


def get_player_pc_position[P: Position](
    cls: Type[P], player_pc: PlayerController
) -> P:
    return cls.from_structs(
        player_pc.Pawn.K2_GetActorLocation(), player_pc.K2_GetActorRotation()
    )


def set_player_pc_position(position: Position, player_pc: UObject) -> None:
    player_pc.Pawn.K2_TeleportTo(
        position.make_vector(),
        position.make_rotator(),
    )
    # TODO: vehicle teleporting


def get_actor_position[P: Position](cls: Type[P], actor: UObject) -> P:
    return cls.from_structs(
        actor.K2_GetActorLocation(), actor.K2_GetActorRotation()
    )


def set_actor_position(position: Position, actor: UObject) -> None:
    actor.K2_TeleportTo(
        position.make_vector(),
        position.make_rotator(),
    )


_DummyVector = make_struct("Vector")
_DummyRotator = make_struct("Rotator")
FastTravelStationComponent = find_class("FastTravelStationComponent")
LevelTravelStationComponent = find_class("LevelTravelStationComponent")


def get_spawns() -> Sequence[Sequence[Position]]:
    fast_travels: list[Position] = []
    level_transitions: list[Position] = []
    respawns: list[Position] = []

    pawn = get_pc().Pawn

    for station in find_all("TravelStationComponentBase", False):
        if (
            station == station.Class.ClassDefaultObject
            or station.Name.endswith("_GEN_VARIABLE")
        ):
            continue

        _, location, rotation = station.GetAvailableSpawnLocation(
            pawn,
            _DummyVector,
            _DummyRotator,
            True,
            False,
        )
        position = _positions.Position.from_structs(location, rotation)

        if station.Class._inherits(FastTravelStationComponent):
            fast_travels.append(position)
        elif station.Class._inherits(LevelTravelStationComponent):
            level_transitions.append(position)
        else:
            respawns.append(position)

    return level_transitions, respawns, fast_travels


def get_speed() -> float:
    return ENGINE.GameViewport.World.PersistentLevel.WorldSettings.TimeDilation


def set_speed(speed: float) -> None:
    ENGINE.GameViewport.World.PersistentLevel.WorldSettings.TimeDilation = (
        speed
    )


def get_freeze() -> bool:
    return get_speed() == 0


def set_freeze(should_freeze: bool) -> None:
    set_speed(0 if should_freeze else 1)
