from . import entry

from types import ModuleType

__windowmodules = (entry,)

def getwindows() -> tuple[ModuleType]:
    return tuple([module.Window for module in __windowmodules])