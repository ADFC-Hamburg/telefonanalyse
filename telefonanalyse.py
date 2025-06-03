#!/usr/bin/env python3

import modules
from common import strings, templates


mainmenu = templates.MainWindow(strings.TITLE,modules.getwindows())
mainmenu.run()
