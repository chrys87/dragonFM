import sys, os, threading, curses, time
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
        self.setProcessName()
        curses.wrapper(self.proceed)
    def proceed(self, screen):
        curses.raw()
        curses.curs_set(1)
        self.screen = screen
        self.screen.leaveok(0)
        self.viewManager = viewManager.viewManager(self.screen, self.settingsManager)
        self.viewManager.update()
        self.inputManager = inputManager.inputManager(self.screen, self.settingsManager)
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

