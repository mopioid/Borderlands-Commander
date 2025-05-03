from .willow2 import *

from .. import _positions

try:
    from ui_utils import show_hud_message
except ImportError:
    show_hud_message = None
try:
    from ui_utils import TrainingBox
except ImportError:
    TrainingBox = None


default_commands = """\
Toggle HUD:
py get_pc().myHUD.ToggleHUD()

Toggle Third Person:
py get_pc().SetBehindView(not get_pc().bBehindView)

Quit Without Saving:
py get_pc().ReturnToTitleScreen()

Respawn Enemies:
py for den in find_all("PopulationOpportunityDen"):
    if den != den.Class.ClassDefaultObject and den.GetNumDied() > 0:
        den.RespawnKilledActors(1.0)
"""


def popup(message: str) -> None:
    if show_hud_message:
        show_hud_message("Commander", message)


def ui_dialog(message: str) -> None:
    if TrainingBox:
        TrainingBox(title="Commander", message=message).show()


def get_player_name(player: PlayerReplicationInfo) -> int:
    return player.PlayerName


def set_player_pc_position(
    position: Position, player_pc: PlayerController
) -> None:
    player_pc.Pawn.Location = position.make_vector()
    player_pc.Rotation = position.make_rotator()
    # TODO: vehicle teleporting


HoldingAreaDestination = find_class("HoldingAreaDestination")
EmergencyTeleportOutpost = find_class("EmergencyTeleportOutpost")


def get_spawns() -> Sequence[Sequence[Position]]:
    fast_travels: list[Position] = []
    level_transitions: list[Position] = []
    respawns: list[Position] = []

    for teleporter in find_all("TeleporterDestination", False):
        if (
            teleporter == teleporter.Class.ClassDefaultObject
            or teleporter.Class._inherits(HoldingAreaDestination)
            or teleporter._path_name().startswith("Loader")
            or len(teleporter.ExitPoints) < 1
        ):
            continue

        position = get_actor_position(
            _positions.Position, teleporter.ExitPoints[0]
        )

        outpost: UObject | None = teleporter.Owner

        if not (outpost and outpost.Class._inherits(EmergencyTeleportOutpost)):
            level_transitions.append(position)
        elif outpost and outpost.bFastTravelEnabled:
            fast_travels.append(position)
        else:
            respawns.append(position)

    return fast_travels, level_transitions, respawns
