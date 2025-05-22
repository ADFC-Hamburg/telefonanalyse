#!/usr/bin/env python3

import modules
from common import templates


TITLE = 'ADFC Telefonanalyse'

mainmenu = templates.MainWindow(TITLE,modules.getwindows())
mainmenu.run()
