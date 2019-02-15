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
        self.screen = None
        self.settingsManager = settingsManager.settingsManager()
        self.debugManager = debugManager.debugManager()
    def start(self):
        curses.wrapper(self.proceed)
    def proceed(self, screen):
        self.screen = screen
        self.inputManager = inputManager.inputManager(self.screen)
        self.viewManager = viewManager.viewManager(self.screen)
        self.viewManager.update()
        while self.running:
            key = self.inputManager.get()
            if not self.handleInput(key):
                self.viewManager.handleInput(key)
            self.viewManager.update()
    def handleInput(self, key):
        return False
    def stop(self):
        self.running = False

