#!/usr/bin/env python
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import sys
import argparse
import commands
import os
from PyQt4 import QtGui, QtCore, uic
from ui.qt_interface import SwitcherWindow

# main entry
if __name__ == "__main__":
    # CLI
    cliparser = argparse.ArgumentParser(description='Switch between Python2 and Python3.')
    cliparser.add_argument("-2", "--python2", help="Enables Python 2", action="store_true")
    cliparser.add_argument("-3", "--python3", help="Enables Python 3", action="store_true")
    
    cliargs = cliparser.parse_args()
    if cliargs.python2 and cliargs.python3:
        print("Error: Multiple versions specified. Please choose one version to switch to.")
    if cliargs.python2:
        os.system("rm %s" % SwitcherWindow.PYTHON_SLINK)
        os.system("ln -s %s %s" % (SwitcherWindow.PYTHON2_PATH, SwitcherWindow.PYTHON_SLINK))
        sys.exit(0)
    if cliargs.python3:
        os.system("rm %s" % SwitcherWindow.PYTHON_SLINK)
        os.system("ln -s %s %s" % (SwitcherWindow.PYTHON3_PATH, SwitcherWindow.PYTHON_SLINK))
        sys.exit(0)
    
    # GUI
    app = QtGui.QApplication(sys.argv)
    win = SwitcherWindow()
    sys.exit(app.exec_())
