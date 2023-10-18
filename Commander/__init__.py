from . import Commander
from Mods import ModMenu #type: ignore

ModMenu.RegisterMod(Commander.Instance)

#TODO Provide instructions if no UserFeedback
