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
sys.path.append('/usr/lib/bbqlinux-python-switcher')
import os
import string

from switcher import SwitcherEngine

from PyQt4 import QtGui, QtCore, uic

class SwitcherWindow(QtGui.QMainWindow):

    PYTHON_SLINK = "/usr/bin/python"

    PYTHON2_EXEC = "python2"
    PYTHON2_PATH = "/usr/bin/"

    PYTHON3_EXEC = "python3"
    PYTHON3_PATH = "/usr/bin/"

    def __init__(self):
        # Check if we run as root
        if os.geteuid() != 0:
            sys.exit('Script must be run as root')

        QtGui.QMainWindow.__init__(self)
        self.ui = uic.loadUi('/usr/share/bbqlinux-python-switcher/qt_interface.ui')

        # Set window title
        self.ui.setWindowTitle("BBQLinux Python Switcher")
        self.ui.setWindowIcon(QtGui.QIcon('/usr/share/bbqlinux/icons/bbqlinux_icon_blue_32x32.png'))

        # Show the window
        self.ui.show()
        
        # Move main window to center
        qr = self.ui.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.ui.move(qr.topLeft())

        # Connect the buttons
        self.connect(self.ui.button_exit, QtCore.SIGNAL("clicked()"), QtGui.qApp, QtCore.SLOT("quit()"))
        self.connect(self.ui.button_python2, QtCore.SIGNAL("clicked()"), self.button_python2_clicked)
        self.connect(self.ui.button_python3, QtCore.SIGNAL("clicked()"), self.button_python3_clicked)

        # Refresh button states
        self.refresh_button_state()

    def refresh_button_state(self):
        python_path = self.get_active_python(self.PYTHON_SLINK)
        if python_path == ("%s%s" % (self.PYTHON2_PATH, self.PYTHON2_EXEC)) or python_path == ("%s" % self.PYTHON2_EXEC):
            self.ui.button_python2.setText(unicode("Active"))
            self.ui.button_python2.setEnabled(False)
            self.ui.button_python3.setText(unicode("Activate"))
            self.ui.button_python3.setEnabled(True)
        elif python_path == ("%s%s" % (self.PYTHON3_PATH, self.PYTHON3_EXEC)) or python_path == ("%s" % self.PYTHON3_EXEC):
            self.ui.button_python3.setText(unicode("Active"))
            self.ui.button_python3.setEnabled(False)
            self.ui.button_python2.setText(unicode("Activate"))
            self.ui.button_python2.setEnabled(True)
        else:
            self.ui.button_python2.setText(unicode("Activate"))
            self.ui.button_python2.setEnabled(True)
            self.ui.button_python3.setText(unicode("Activate"))
            self.ui.button_python3.setEnabled(True)
            
        # Deactivates buttons for python versions not installed / missing
        if not os.path.isfile(("%s%s" % (self.PYTHON2_PATH, self.PYTHON2_EXEC))):
            self.ui.button_python2.setText(unicode("Not Found"))
            self.ui.button_python2.setEnabled(False)
        if not os.path.isfile(("%s%s" % (self.PYTHON3_PATH, self.PYTHON2_EXEC))):
            self.ui.button_python3.setText(unicode("Not Found"))
            self.ui.button_python3.setEnabled(False)

    def button_python2_clicked(self):
        os.system("rm %s" % self.PYTHON_SLINK)
        os.system("ln -s %s%s %s" % (self.PYTHON2_PATH, self.PYTHON2_EXEC, self.PYTHON_SLINK))
        self.refresh_button_state()

    def button_python3_clicked(self):
        os.system("rm %s" % self.PYTHON_SLINK)
        os.system("ln -s %s %s" % (self.PYTHON3_PATH, self.PYTHON3_EXEC, self.PYTHON_SLINK))
        self.refresh_button_state()

    def get_active_python(self, link):
        try:
            path = os.readlink(link)
            return path
        except Exception: 
            pass
