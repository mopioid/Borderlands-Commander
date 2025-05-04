from unrealsdk import find_all, find_class, find_enum, make_struct
from unrealsdk.unreal import UObject

from mods_base import ENGINE, get_pc

from .. import _positions

from ui_utils import show_hud_message, TrainingBox

from math import tau

from typing import Sequence, Type


Angle = int
type Position = "_positions.Position"
type PlayerController = UObject
type PlayerReplicationInfo = UObject
ENetMode = find_enum("ENetMode")

default_gameinfo = find_class("WillowCoopGameInfo").ClassDefaultObject


default_commands = """\
Toggle HUD:
py get_pc().myHUD.ToggleHUD()

Toggle Third Person:
py get_pc().SetBehindView(not get_pc().bBehindView)

Quit Without Saving:
py get_pc().ReturnToTitleScreen(True, False)

Respawn Enemies:
set PopulationOpportunityDen bIsWaitingForRespawn True
set PopulationOpportunityDen RespawnDelayStartTime -10000
"""


def console_command(command: str) -> None:
    get_pc().ConsoleCommand(command)


def popup(message: str) -> None:
    show_hud_message("Commander", message)


def ui_dialog(message: str) -> None:
    TrainingBox(title="Commander", message=message).show()


def is_client() -> bool:
    return ENGINE.GetCurrentWorldInfo().NetMode == ENetMode.NM_Client


def get_players() -> Sequence[PlayerReplicationInfo]:
    return ENGINE.GetCurrentWorldInfo().GRI.PRIArray


def get_player_pc(player: PlayerReplicationInfo) -> PlayerController:
    return player.Owner


def get_player_id(player: PlayerReplicationInfo) -> int:
    return player.PlayerID


def get_player_name(player: PlayerReplicationInfo) -> int:
    return player.PlayerNameHTML


def to_radians(angle: Angle) -> float:
    return float(angle) / 65535.0 * tau


def from_radians(radians: float) -> Angle:
    return Angle(radians * 65535.0 / tau)


def get_map() -> str:
    return ENGINE.GetCurrentWorldInfo().GetMapName(True)


def get_player_pc_position[P: Position](
    cls: Type[P], player_pc: PlayerController
) -> P:
    return cls.from_structs(player_pc.Pawn.Location, player_pc.Rotation)


def get_actor_position[P: Position](cls: Type[P], actor: UObject) -> P:
    return cls.from_structs(actor.Location, actor.Rotation)


def set_player_pc_position(
    position: Position, player_pc: PlayerController
) -> None:
    location = position.make_vector()
    rotation = position.make_rotator()

    _, vehicle = player_pc.IsUsingVehicleEx(True, None)
    if vehicle:
        pawn = vehicle.GetPawnToTeleport()
        pawn.Mesh.SetRBPosition(location)
        pawn.Mesh.SetRBRotation(rotation)
    else:
        player_pc.Pawn.Location = location
        player_pc.ClientSetRotation(rotation)
        player_pc.Pawn.Velocity = make_struct("Vector")


def get_spawns() -> Sequence[Sequence[Position]]:
    fast_travels: list[Position] = []
    level_transitions: list[Position] = []
    respawns: list[Position] = []

    FastTravelStation = find_class("FastTravelStation")
    LevelTravelStation = find_class("LevelTravelStation")

    for station in find_all("TravelStation", False):
        if (
            station == station.Class.ClassDefaultObject
            or len(station.TeleportDest.ExitPoints) < 1
        ):
            continue

        position = get_actor_position(
            _positions.Position, station.TeleportDest.ExitPoints[0]
        )

        if station.Class._inherits(FastTravelStation):
            fast_travels.append(position)
        elif station.Class._inherits(LevelTravelStation):
            level_transitions.append(position)
        else:
            respawns.append(position)

    return fast_travels, level_transitions, respawns


def get_speed() -> float:
    return default_gameinfo.GameSpeed


def set_speed(speed: float) -> None:
    default_gameinfo.GameSpeed = speed
    ENGINE.GetCurrentWorldInfo().TimeDilation = speed


def set_freeze(should_freeze: bool) -> None:
    ENGINE.GetCurrentWorldInfo().bPlayersOnly = should_freeze


def get_freeze() -> bool:
    return ENGINE.GetCurrentWorldInfo().bPlayersOnly
