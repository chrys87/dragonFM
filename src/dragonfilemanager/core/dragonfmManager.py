import sys, os, threading, curses, time
from dragonfilemanager.core import i18n
from dragonfilemanager.core import settingsManager
from dragonfilemanager.core import debugManager
from dragonfilemanager.core import viewManager
from dragonfilemanager.core import inputManager

class dragonfmManager():
    def __init__(self):
        self.running = True
        self.timer = threading.Thread(target=self.timerTrigger)
        self.screen = None
        self.settingsManager = settingsManager.settingsManager()
        self.debugManager = debugManager.debugManager()
    def start(self):
        curses.wrapper(self.proceed)
    def proceed(self, screen):
        self.screen = screen
        self.viewManager = viewManager.viewManager(self.screen)
        self.viewManager.update()
        self.inputManager = inputManager.inputManager(self.screen)
        self.timer.start()
        while self.running:
            key = self.inputManager.get()
            if not self.handleInput(key):
                self.viewManager.handleInput(key)
            if self.running:
                try:
                    self.viewManager.update()
                except:
                    pass
        self.shutdown()
    def handleInput(self, key):
        if key == 'q':
            self.stop()
            return True
        return False
    def timerTrigger(self):
        while self.running:
            time.sleep(0.5)
            try:
                self.viewManager.update()
            except:
                pass

    def stop(self):
        self.running = False
    def shutdown(self):
        if self.timer:
            self.timer.join()




