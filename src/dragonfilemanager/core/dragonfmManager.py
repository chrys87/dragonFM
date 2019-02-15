import sys,os
import curses

from dragonfilemanager.core import i18n
from dragonfilemanager.core import settingsManager
from dragonfilemanager.core import debugManager
from dragonfilemanager.core import viewManager
from dragonfilemanager.core import inputManager

class dragonfmManager():
    def __init__(self):
        self.running = True
        self.inputManager = inputManager.inputManager()
        self.viewManager = viewManager.viewManager()
        self.settingsManager = settingsManager.settingsManager()
        self.debugManager = debugManager.debugManager()
    def proceed(self):
        while self.running:
            viewManager.update()
