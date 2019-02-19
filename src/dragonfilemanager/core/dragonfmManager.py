import sys, os, threading, curses, time
from dragonfilemanager.core import i18n
from dragonfilemanager.core import settingsManager
from dragonfilemanager.core import debugManager
from dragonfilemanager.core import viewManager
from dragonfilemanager.core import inputManager

class dragonfmManager():
    def __init__(self):
        self.running = False
        self.screen = None
        self.settingsManager = None
        self.debugManager = None
        self.height = 0
        self.width = 0
        self.setProcessName()
    def start(self):
        self.running = True
        curses.wrapper(self.proceed)
    # main process
    def proceed(self, screen):
        self.setScreen(screen)
        if not screen:
            return
        self.debugManager = debugManager.debugManager(self)
        self.settingsManager = settingsManager.settingsManager(self)
        self.screen.leaveok(0)
        curses.raw()
        curses.curs_set(1)
        self.viewManager = viewManager.viewManager(self)
        self.inputManager = inputManager.inputManager(self)
        self.viewManager.update()
        while self.running:
            key = self.inputManager.get()
            if key:
                if not self.handleInput(key):
                    self.viewManager.handleInput(key)
            self.viewManager.update()
        self.shutdown()
    def handleInput(self, key):
        if key == 'q':
            self.stop()
            return True
        return False

    def stop(self):
        self.running = False
    def shutdown(self):
        pass
    def setScreen(self, screen):
        if not screen:
            return
        self.screen = screen
        self.height, self.width = self.screen.getmaxyx()
    def setProcessName(self, name = 'dragonFM'):
        """Attempts to set the process name to 'dragonFM'."""
        # Disabling the import error of setproctitle.
        # pylint: disable-msg=F0401
        try:
            from setproctitle import setproctitle
        except ImportError:
            pass
        else:
            setproctitle(name)
            return True

        try:
            from ctypes import cdll, byref, create_string_buffer
            libc = cdll.LoadLibrary('libc.so.6')
            stringBuffer = create_string_buffer(len(name) + 1)
            stringBuffer.value = bytes(name, 'UTF-8')
            libc.prctl(15, byref(stringBuffer), 0, 0, 0)
            return True
        except:
            pass
        return False

    def move(self, y, x):
        self.screen.move(y, x)
    def refresh(self):
        self.screen.refresh()
    def clear(self):
        self.screen.clear()
    # getter
    def getScreenWidth(self):
        return self.width
    def getScreenHeight(self):
        return self.height
    def getSettingsManager(self):
        return self.settingsManager
    def getViewManager(self):
        return self.viewManager
    def getInputManager(self):
        return self.inputManager
    def getDebugManager(self):
        return self.debugManager
    def getScreen(self):
        return self.screen
