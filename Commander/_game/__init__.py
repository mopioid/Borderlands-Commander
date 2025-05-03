from mods_base import Game, Mod

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .oak import *
elif Game.get_current().name == "BL1":
    from .bl1 import *
elif Game.get_tree().name == "Willow2":
    from .willow2 import *
elif Game.get_tree().name == "Oak":
    from .oak import *
try:
    from console_mod_menu.screens import screen_stack as console_screens
except ImportError:
    console_screens = ()


mod: Mod


def dialog(message: str) -> None:
    if console_screens:
        print(f"\n[ Commander ]\n{message}\n")
    else:
        ui_dialog(message)
