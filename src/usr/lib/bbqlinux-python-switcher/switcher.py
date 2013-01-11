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

import os
import subprocess
from subprocess import Popen
import time
import shutil
import gettext
import stat
import traceback
import commands
import sys
from PyQt4 import QtCore

class SwitcherEngine(QtCore.QThread):
    ''' This is central to the bbqlinux installer '''

    def __init__(self, setup, parent = None):
        QtCore.QThread.__init__(self, parent)

    def __del__(self):
        self.wait()

    def run(self):
        self.install(self.setup)
