from . import entry, export

from types import ModuleType

__windowmodules = (entry, export)

def getwindows() -> tuple[ModuleType]:
    return tuple([module.Window for module in __windowmodules])